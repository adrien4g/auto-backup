docker inspect onedrive > /dev/null && docker rm -f onedrive

docker run -d \
	--restart unless-stopped     \
	-e ONEDRIVE_VERBOSE=1         \
	-e ONEDRIVE_RESYNC=1           \
	-v onedrive_conf:/onedrive/conf \
	-v /home/vagrant:/onedrive/data  \
	--name onedrive                   \
	driveone/onedrive
