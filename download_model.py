from huggingface_hub import snapshot_download

print("🚀 開始下載 Qwen2.5-Coder-7B-Instruct 模型...")
print("檔案有點大 (約 15GB)，請耐心等候...")

snapshot_download(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    local_dir="./models/base_qwen_7b",
    local_dir_use_symlinks=False
)

print("✅ 模型下載完成！")
