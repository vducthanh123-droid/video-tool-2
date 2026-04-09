# Video Tool - GitHub Actions Build Ready

Repo này đã sẵn cấu trúc để build gui_pro.exe bằng GitHub Actions trên Windows.

## File cần có ở root repo
- gui_pro.py
- ffmpeg.exe

## File workflow
- .github/workflows/build.yml

## Cách dùng
1. Tạo repo GitHub mới
2. Upload toàn bộ file trong gói này
3. Upload thêm ffmpeg.exe vào root repo
4. Vào tab Actions
5. Chọn Build EXE
6. Bấm Run workflow
7. Tải artifact video-tool-exe

## Output
- gui_pro.exe

## Lưu ý
- Bản này dùng openai-whisper, không dùng whisperx
- Máy local của bạn không cần Python 3.11 để build
- GitHub Actions sẽ tự dùng Python 3.11 trên máy Windows của GitHub
