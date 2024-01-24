variable "ANALYTICS_BASE_URL" {
  description = "value"
  type        = string
}

/* ------------------------ Analytics and Sourcing Auth Flow ------------------------ */

variable "PARMA_SHARED_SECRET_KEY" {
  description = "Shared secret key for the analytics and sourcing auth flow"
  type        = string
  sensitive   = true
}

/* ------------------------------------ Discord ------------------------------------ */

variable "DISCORD_BASE_URL" {
  description = "Discord base url"
  type        = string
  sensitive   = false
}

variable "DISCORD_AUTH_KEY" {
  description = "Discord auth key"
  type        = string
  sensitive   = true
}
