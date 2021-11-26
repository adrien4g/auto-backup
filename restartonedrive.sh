docker inspect onedrive > /dev/null && docker rm -f onedrive
backup_dir=$(awk -F "=" '/backup_dir/ {print $2}' config.ini)/backup

docker run -d \
	--restart unless-stopped     \
	-e ONEDRIVE_VERBOSE=1         \
	-e ONEDRIVE_RESYNC=1           \
	-v onedrive_conf:/onedrive/conf \
	-v $backup_dir:/onedrive/data  \
	--name onedrive                   \
	driveone/onedrive
