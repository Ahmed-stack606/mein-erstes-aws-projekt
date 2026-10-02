import argparse
from fleetpulse.services.telemetry import generate_telemetry, write_telemetry

def main() -> None:
    parser = argparse.ArgumentParser(description="FleetPulse CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    gen = sub.add_parser("generate-data")
    gen.add_argument("--vehicles", type=int, default=250)
    gen.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()
    if args.command == "generate-data":
        df = generate_telemetry(args.vehicles, args.hours)
        path = write_telemetry(df)
        print(f"Generated {len(df):,} telemetry rows -> {path}")

if __name__ == "__main__":
    main()
