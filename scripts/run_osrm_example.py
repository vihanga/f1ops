#!/usr/bin/env python3
"""
Example script demonstrating OSRM routing integration.

This script shows how to use OSRM for more accurate road distance calculations.
You can run your own OSRM server with Docker or use the public demo server.

To run a local OSRM server:
    docker run -t -i -p 5000:5000 osrm/osrm-backend osrm-routed --algorithm mld /data/europe.osrm

Set environment variable:
    export OSRM_BASE_URL=http://localhost:5000
    export USE_OSRM=true

Then run this script:
    python scripts/run_osrm_example.py --season 2019
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from f1ops.config import OSRM_BASE_URL, USE_OSRM
from f1ops.data_loader import get_european_races
from f1ops.geo import build_season_legs


def main() -> None:
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="OSRM routing example")
    parser.add_argument("--season", type=int, default=2019, help="Season year (default: 2019)")
    parser.add_argument(
        "--osrm-url",
        type=str,
        default=OSRM_BASE_URL,
        help=f"OSRM server URL (default: {OSRM_BASE_URL})",
    )
    args = parser.parse_args()

    # Check OSRM configuration
    use_osrm = os.getenv("USE_OSRM", "false").lower() == "true" or args.osrm_url != OSRM_BASE_URL

    print("F1Ops OSRM Integration Example")
    print("=" * 50)
    print(f"Season: {args.season}")
    print(f"OSRM URL: {args.osrm_url}")
    print(f"OSRM Enabled: {use_osrm}")
    print()

    if not use_osrm:
        print("NOTE: OSRM is not enabled. Set USE_OSRM=true to enable.")
        print("      Using Haversine distance estimation instead.")
        print()

    # Load races
    try:
        races = get_european_races(args.season)
        print(f"Found {len(races)} European races for {args.season}")
        print()

        # Build legs with OSRM if enabled
        legs = build_season_legs(races, use_osrm=use_osrm)

        # Display results
        print(f"{'Leg':<5} {'From → To':<40} {'Distance (km)':<15} {'Method':<10}")
        print("-" * 70)

        total_distance = 0
        osrm_count = 0

        for idx, leg in enumerate(legs):
            print(f"{idx+1:<5} {leg.leg_name:<40} {leg.distance_km:<15.2f} {leg.method:<10}")
            total_distance += leg.distance_km
            if leg.method == "osrm":
                osrm_count += 1

        print("-" * 70)
        print(f"Total distance: {total_distance:.2f} km")
        print(f"OSRM routes: {osrm_count}/{len(legs)}")
        print(f"Haversine routes: {len(legs) - osrm_count}/{len(legs)}")

        if use_osrm and osrm_count == 0:
            print()
            print("WARNING: OSRM was enabled but no routes were calculated via OSRM.")
            print("         This may indicate the OSRM server is not reachable.")
            print(f"         Check that {args.osrm_url} is accessible.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease run create_sample_data.py first to generate calendar data.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
