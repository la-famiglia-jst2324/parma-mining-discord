"""Normalization map for discord data."""


class DiscordNormalizationMap:
    """Normalization map for discord data."""

    map_json = {
        "Source": "discord",
        "Mappings": [
            {
                "SourceField": "id",
                "DataType": "text",
                "MeasurementName": "server id",
            },
            {
                "SourceField": "name",
                "DataType": "text",
                "MeasurementName": "server name",
            },
            {
                "SourceField": "description",
                "DataType": "paragraph",
                "MeasurementName": "server description",
            },
            {
                "SourceField": "features",
                "DataType": "text",
                "MeasurementName": "server features",
            },
            {
                "SourceField": "owner_id",
                "DataType": "text",
                "MeasurementName": "server owner id",
            },
            {
                "SourceField": "region",
                "DataType": "text",
                "MeasurementName": "server region",
            },
            {
                "SourceField": "max_presences",
                "DataType": "int",
                "MeasurementName": "server max presences",
            },
            {
                "SourceField": "max_members",
                "DataType": "int",
                "MeasurementName": "server max members",
            },
            {
                "SourceField": "preferred_locale",
                "DataType": "text",
                "MeasurementName": "server language code",
            },
            {
                "SourceField": "premium_tier",
                "DataType": "int",
                "MeasurementName": "server premium tier",
            },
            {
                "SourceField": "premium_subscription_count",
                "DataType": "int",
                "MeasurementName": "server premium subscription count",
            },
            {
                "SourceField": "approximate_member_count",
                "DataType": "int",
                "MeasurementName": "server member count",
            },
            {
                "SourceField": "approximate_presence_count",
                "DataType": "int",
                "MeasurementName": "server active member count",
            },
        ],
    }

    def get_normalization_map(self) -> dict:
        """Return the normalization map."""
        return self.map_json
