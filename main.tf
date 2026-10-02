provider "aws" {
  region = "eu-central-1"
}

resource "aws_s3_bucket" "mein_erstes_bucket" {
  bucket = "ahmed-stack606-lime-projekt-2026"
}

# Das ist ein S3 Bucket - wie eine Festplatte in der Cloud
# Hier würden bei Lime die Bilder von den Scootern liegen
