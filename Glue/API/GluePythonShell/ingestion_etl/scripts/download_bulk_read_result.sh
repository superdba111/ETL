#data.download_url => https://www.zohoapis.com<download_url>
curl "https://www.zohoapis.com/crm/bulk/v3/read/4776181000001445001/result" \
-X GET \
-H "Authorization: Zoho-oauthtoken 1000.XXXXX" \
--output "download_file_csv_bin.txt"