from modelscope import snapshot_download

# Specify the model ID and the directory where you want to save the model
model_id = 'iic/DocOwl1.5-Chat'
save_dir = './chatmodel'

# Download the model
model_dir = snapshot_download(model_id, cache_dir=save_dir)

print(f"Model has been saved to: {model_dir}")
