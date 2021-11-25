mkdir -p /home/$USER/backup

docker run -it \
	--restart unless-stopped     \
	-e ONEDRIVE_VERBOSE=1         \
	-e ONEDRIVE_RESYNC=1           \
	-v onedrive_conf:/onedrive/conf \
	-v /home/ntm/backup:/onedrive/data  \
	--name onedrive                   \
	driveone/onedrive
