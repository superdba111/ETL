 curl "https://www.zohoapis.com/crm/bulk/v3/read" \
-X POST \
-H "Authorization: Zoho-oauthtoken 1000.XXXXXX" \
-H "Content-Type: application/json" \
-d "@inputData.json"