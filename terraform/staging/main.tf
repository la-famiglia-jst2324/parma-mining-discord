terraform {
  required_version = "1.5.3"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
  backend "gcs" {
    bucket      = "la-famiglia-jst2324-tf-state"
    prefix      = "terraform/state/staging/mining/discord"
    credentials = "../.secrets/la-famiglia-parma-ai.json"
  }
}

locals {
  project = "la-famiglia-parma-ai"
  region  = "europe-west1"
}

provider "google" {
  credentials = file("../.secrets/la-famiglia-parma-ai.json")
  project     = local.project
  region      = local.region
}

module "main" {
  source             = "../module"
  env                = "staging"
  project            = local.project
  region             = local.region
  ANALYTICS_BASE_URL = var.ANALYTICS_BASE_URL

  PARMA_SHARED_SECRET_KEY = var.PARMA_SHARED_SECRET_KEY

  DISCORD_BASE_URL = var.DISCORD_BASE_URL
  DISCORD_AUTH_KEY = var.DISCORD_AUTH_KEY
}
