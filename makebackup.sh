project_folder=$(dirname "$(realpath $0)")
cd $project_folder/backup_manager
source .env/bin/activate
python3 main.py
chown -R ntm:ntm $project_folder
