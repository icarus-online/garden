#!/usr/bin/env python3
"""Read-only public DNS, certificate, HTTP, security-header, and release-health checks."""
import argparse
import json
import re
import socket
import ssl
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def request(url):
    opener = build_opener(NoRedirect)
    try:
        response = opener.open(Request(url,headers={'User-Agent':'GardenHealth/1.0','Accept':'*/*'}),timeout=15)
    except HTTPError as error:
        response = error
    with response:
        body = response.read(1024 * 1024 + 1)
        if len(body) > 1024 * 1024:
            raise ValueError('Response exceeds monitor size limit')
        return response.status, response.headers, body

def require_headers(headers):
    required = {'x-content-type-options':'nosniff','x-frame-options':'DENY',
        'referrer-policy':'strict-origin-when-cross-origin'}
    for key, expected in required.items():
        if headers.get(key) != expected:
            raise ValueError(f'Unexpected or absent {key}')
    if 'max-age=' not in headers.get('strict-transport-security',''):
        raise ValueError('HSTS absent')
    csp = headers.get('content-security-policy','')
    for directive in ("script-src 'self'", "style-src 'self'", "connect-src 'self'", "frame-ancestors 'none'"):
        if directive not in csp:
            raise ValueError(f'CSP lacks {directive}')
    if 'unsafe-inline' in csp or 'unsafe-eval' in csp or '*' in csp:
        raise ValueError('CSP contains an unsafe execution policy')
    if not headers.get('permissions-policy') or headers.get('set-cookie') or headers.get('server'):
        raise ValueError('Unexpected cookie/server header or absent permissions policy')

def check(host, expected_ip=None, expected_revision=None, min_cert_days=14):
    if not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9.-]*',host):
        raise ValueError('Supply a hostname only')
    addresses = sorted({item[4][0] for item in socket.getaddrinfo(host,443,type=socket.SOCK_STREAM)})
    if not addresses or (expected_ip and expected_ip not in addresses):
        raise ValueError('DNS does not contain the expected production address')
    context = ssl.create_default_context()
    with socket.create_connection((host,443),timeout=15) as stream:
        with context.wrap_socket(stream,server_hostname=host) as connection:
            certificate = connection.getpeercert()
            expires = ssl.cert_time_to_seconds(certificate['notAfter'])
            remaining = (expires-time.time())/86400
            if remaining < min_cert_days:
                raise ValueError(f'Certificate expires in {remaining:.1f} days')
    results = []
    for scheme, path, expected in [
        ('https','/',200),('https','/health.json',200),
        ('https','/index.html?garden_probe=canonical',308),
        ('http','/laboratory.html?garden_probe=https',308),
        ('https','/__garden_healthcheck_missing__',404),
        ('https','/.env',404),('https','/.git/config',404),('https','/assets/',404)]:
        status, headers, body = request(f'{scheme}://{host}{path}')
        if status != expected:
            raise ValueError(f'{scheme} {path}: expected {expected}, received {status}')
        require_headers(headers)
        if path == '/':
            if b'The Garden' not in body:
                raise ValueError('Homepage identity missing')
        elif path == '/health.json':
            health = json.loads(body)
            if (health.get('status') != 'ok' or health.get('project') != 'garden'
                or health.get('research_status') != 'pre-pilot_no_results' or health.get('inference_enabled') is not False):
                raise ValueError('Unexpected release health/research state')
            if not re.fullmatch('[a-f0-9]{40}',health.get('source_revision','')):
                raise ValueError('Missing full source revision')
            if expected_revision and health['source_revision'] != expected_revision:
                raise ValueError('Wrong deployed source revision')
            if 'no-store' not in headers.get('cache-control',''):
                raise ValueError('Health response must not be cached')
        elif status == 308:
            location = headers.get('location','')
            if scheme == 'http' and location != f'https://{host}{path}':
                raise ValueError('HTTP canonical redirect did not preserve path/query')
            if scheme == 'https' and location not in ('/?garden_probe=canonical',f'https://{host}/?garden_probe=canonical'):
                raise ValueError('Index redirect did not preserve query')
        results.append({'scheme':scheme,'path':path,'status':status,'security_headers':'passed'})
    return {'status':'passed','checked_utc':datetime.now(timezone.utc).isoformat(),'host':host,'dns_addresses':addresses,
        'certificate_not_after':certificate['notAfter'],'certificate_days_remaining':round(remaining,1),
        'source_revision':health['source_revision'],'checks':results,
        'scope':'Public endpoint checks only; this does not verify mail routing, authoritative DNSSEC, internal isolation, or research outcomes.'}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',default='garden.icarus.onl')
    parser.add_argument('--expected-ip')
    parser.add_argument('--expected-revision')
    parser.add_argument('--min-cert-days',type=int,default=14)
    args=parser.parse_args()
    try:
        result=check(args.host,args.expected_ip,args.expected_revision,args.min_cert_days)
    except (OSError,ValueError,URLError,KeyError) as error:
        print(json.dumps({'status':'failed','host':args.host,'error':str(error)}))
        return 1
    print(json.dumps(result,indent=2))
    return 0

if __name__ == '__main__':
    sys.exit(main())
