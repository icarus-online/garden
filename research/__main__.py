"""Command line interface for reproducible local apparatus checks."""
import argparse
import json
import sys
from pathlib import Path
from .core import IntegrityError, blind, check_lock, load_json, make_lock, run, verify, write_json

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('lock', 'validate', 'run'):
        command = commands.add_parser(name)
        command.add_argument('config', type=Path)
        command.add_argument('--lock', type=Path, help='Defaults to CONFIG with .lock.json suffix')
        if name == 'run':
            command.add_argument('--out', type=Path, required=True)
    command = commands.add_parser('verify')
    command.add_argument('run_dir', type=Path)
    command = commands.add_parser('blind')
    command.add_argument('run_dir', type=Path)
    command.add_argument('--out', type=Path, required=True)
    command.add_argument('--key-out', type=Path, required=True, help='New private key file outside review directory')
    args = parser.parse_args(argv)
    try:
        if args.command in ('lock', 'validate', 'run'):
            config = load_json(args.config)
            lock_path = args.lock or args.config.with_suffix('.lock.json')
            if args.command == 'lock':
                lock = make_lock(config)
                with lock_path.open('xb') as f:
                    from .core import canonical
                    f.write(canonical(lock))
                lock_path.chmod(0o600)
                result = {'status':'locked_dry_run_config','lock':str(lock_path),'config_sha256':lock['config_sha256']}
            else:
                lock = load_json(lock_path)
                check_lock(config, lock)
                result = run(config, lock, args.out) if args.command == 'run' else {'status':'valid_dry_run_config','config_sha256':lock['config_sha256']}
        elif args.command == 'verify':
            result = verify(args.run_dir)
        else:
            result = blind(args.run_dir, args.out, args.key_out)
        print(json.dumps({k:v for k,v in result.items() if k not in ('artifacts','implementation_sha256')}, indent=2))
        return 0
    except (IntegrityError, ValueError, OSError, KeyError, TypeError) as error:
        print(f'Garden stopped: {error}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
