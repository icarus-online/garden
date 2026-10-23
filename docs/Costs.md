# Operating and inference costs

**Planning baseline, 22 October 2026.** Platform delivery does not authorize a paid research pilot. No live model provider or participant model is configured, and the local apparatus makes no inference calls.

| Item | Current basis | Increment attributable to this implementation |
|---|---|---|
| Corporate DigitalOcean Droplet | Existing audited 1-vCPU/1-GB host, $6/month compute plan | No new Droplet or resize; $0 additional fixed compute commitment |
| Caddy / static serving | Existing shared edge and disk | No additional software service or subscription |
| Route 53 | Existing authoritative hosted zone | No new zone; additional query usage remains subject to the existing account's billing |
| TLS | Existing Caddy automatic public certificate management | No purchased certificate introduced |
| GitHub CI / monitoring | Installed standard hosted Linux workflow definitions; run outcomes verified separately | Public-repository standard runner minutes are free under current GitHub policy; artifact/storage usage and private-repository limits must still be checked |
| Research dry runs | Local Python standard library, 624 mechanical records in a full demonstration | $0 provider-inference spend |
| Live study | Not configured, authorized as a separate milestone | Not incurred or estimated as an approved commitment |

DigitalOcean's published basic-plan table lists 1 GiB memory, one vCPU, 25 GiB SSD, and 1,000 GiB transfer at $6/month; this matches the audited plan. The full shared host bill is not a Garden-only allocation, and backups, taxes, transfer overages, or unrelated services may appear separately. Reusing existing capacity avoids a new fixed compute charge but does not guarantee zero incremental usage costs. [DigitalOcean Droplet pricing](https://www.digitalocean.com/pricing/droplets).

The installed `.github/workflows/ci.yml` and `.github/workflows/monitor.yml` use standard hosted Linux runners. CI has a 20-minute job limit and 14-day release-artifact retention; the public health job has a five-minute limit and a configured six-hour schedule. They do not provision paid larger runners, a paid monitoring service, or new production credentials. Public standard-runner minutes are currently free; organization visibility, storage, and billing settings remain authoritative. Installed workflow source does not establish successful execution, delivered alerts, or zero artifact-storage charges. Confirm those facts from actual runs and account usage; the preparation session has not treated a proposed or running job as a completed verification. [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions).

## Future pilot worksheet

The proposed feasibility pilot has 48 trajectories × 13 sessions = **624 scheduled model invocations**. A diagnostic receipt is not a model invocation. Retried attempts, tool continuations, summaries, judge calls, and additional sessions would increase the real count and must be separately logged and capped.

Once a participant provider/model and tokenizer are selected, measure assembled input tokens by phase, output/reasoning-token usage, memory growth, retries, and the provider's actual billing units. For a provider quoting per-million-token prices, the base estimate is:

```text
base cost = total billable input tokens / 1,000,000 × input rate
          + total billable output tokens / 1,000,000 × output rate
          + separately priced reasoning/cache/tool/storage components
```

For arithmetic illustration only, an average of 3,000 input tokens and 800 output tokens across 624 calls would be 1.872 million input and 0.4992 million output tokens. This is not a measured Garden workload or a provider quote. Multiply those quantities by the selected model's verified rates, then add a prespecified bounded retry allowance and other billable components. Do not assume token counts from characters, constant memory length, free reasoning tokens, or that temperature zero eliminates variation.

Before any live run, freeze the exact participant model/version and rates, per-request token limits, maximum attempt count, total monetary cap, funding owner, alert destination, and stop behavior. No automatic fallback to another model is permitted. A higher-cost model, enlarged study, public inference endpoint, new hosting service, or material recurring cost needs its own explicit decision.

## Capacity and cost review

The preparation audit observed approximately 512 MB available memory and 21 GB available disk on the shared corporate host. Static content adds little application memory, but release retention consumes disk and traffic consumes the shared transfer allowance. These figures are dated observations, not guarantees. Retain current and previous known-good releases, inspect disk usage before promotion, and review the existing DigitalOcean and DNS bills after launch. Do not resize or add backups, monitoring products, or inference services automatically in response to this document.
