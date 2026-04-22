import argparse
import pandas as pd
import numpy as np
import yaml
import json
import logging
import time
import sys
import os

def setup_logger(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def write_error(output_path, version, message):
    error_output = {
        "version": version,
        "status": "error",
        "error_message": message
    }
    with open(output_path, "w") as f:
        json.dump(error_output, f, indent=2)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--log-file", required=True)

    args = parser.parse_args()
    setup_logger(args.log_file)
    start_time = time.time()
    try:
        logging.info("Job started")

        if not os.path.exists(args.config):
            raise Exception("Config file not found")

        with open(args.config, "r") as f:
            config = yaml.safe_load(f)

        for key in ["seed", "window", "version"]:
            if key not in config:
                raise Exception(f"Missing config key: {key}")

        seed = config["seed"]
        window = config["window"]
        version = config["version"]

        np.random.seed(seed)
        logging.info(f"Config loaded: {config}")

        if not os.path.exists(args.input):
            raise Exception("file not found")

        try:
            df = pd.read_csv(args.input, sep=",", engine="python")
        except Exception:
            raise Exception("Invalid format")

        if df.empty:
            raise Exception("Dataset empty")

        if "close" not in df.columns:
            raise Exception("Missing 'close' column")

        logging.info(f"Rows loaded: {len(df)}")
        df["rolling_mean"] = df["close"].rolling(window=window).mean()
        df["signal"] = (df["close"] > df["rolling_mean"]).astype(int)
        df_valid = df.dropna()
        logging.info("Rolling mean and signal computed")

        rows_processed = len(df_valid)
        signal_rate = df_valid["signal"].mean()
        latency_ms = int((time.time() - start_time) * 1000)

        result = {
            "version": version,
            "rows_processed": rows_processed,
            "metric": "signal_rate",
            "value": round(float(signal_rate),2),
            "latency_ms": latency_ms,
            "seed": seed,
            "status": "success"
        }

        with open(args.output, "w") as f:
            json.dump(result,f,indent=2)

        logging.info(f"Metrics: {result}")
        logging.info("successfull")

        print(json.dumps(result,indent=2))
        sys.exit(0)

    except Exception as e:
        logging.error(str(e))

        version = "unknown"
        if "config" in locals() and "version" in config:
            version = config["version"]

        write_error(args.output,version,str(e))

        print(f"Error:{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()