# convert-sc-design-hblab

`convert-sc-design-hblab` là skill dạng repo, tương thích với `skills.sh`.

## Bắt đầu nhanh

Repo này hiện đã bao gồm cấu trúc tương thích `skills.sh` tại `skills/convert-sc-design-hblab/`.

Khi repo được public, có thể cài đặt bằng luồng CLI của Vercel:

```bash
npx skills add https://github.com/datht-hblab-company/convert-sc-design-hblab --skill convert-sc-design-hblab
```

Cách cài này dành cho hệ sinh thái `skills.sh` của Vercel.

Khi skill được sử dụng, nó có thể đọc Google Sheets URL, tự tách `gid`, rồi convert đúng sheet tương ứng. Mọi file markdown được tạo ra nên được ghi vào thư mục `./docs` của workspace hiện tại.

## Ví dụ prompt cho skill `convert-sc-design-hblab`

Có thể hướng dẫn agent bằng prompt như sau khi muốn viết lại nội dung từ Google Sheet vào một file markdown duy nhất. Vì skill hỗ trợ tự đọc `gid` từ URL, nên trong nhiều trường hợp không cần chỉ định tên sheet riêng nếu link đã trỏ đúng tab cần lấy:

```text
Dùng skill convert-sc-design-hblab đọc nội dung trong link Google Sheet này. Không tóm tắt hoặc lược bỏ nội dung.
Gộp toàn bộ nội dung reference vào cùng 1 file markdown trong thư mục ./docs.
```

## Ví dụ với link cụ thể

```text
Dùng skill convert-sc-design-hblab đọc nội dung trong link này:
https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit#gid=<GID>

Yêu cầu:
- Tự đọc `gid` từ link và convert đúng sheet đang được mở trong URL
- Đọc luôn các sheet được reference trong sheet này
- Đưa toàn bộ nội dung reference vào trong cùng 1 file
- Xuất kết quả ra file `./docs/sm-preview-site-recruitment-lp.md`
- Không tóm tắt hoặc lược bỏ nội dung
```

## Công cụ được hỗ trợ

| Công cụ      | Đường dẫn global                               | Đường dẫn project-local          |
| ------------ | ---------------------------------------------- | -------------------------------- |
| Claude Code  | `~/.claude/skills/convert-sc-design-hblab`     | `./.claude/skills/convert-sc-design-hblab` |
| Cursor       | `~/.cursor/skills/convert-sc-design-hblab`     | `./.cursor/skills/convert-sc-design-hblab` |
| Codex        | `~/.codex/skills/convert-sc-design-hblab`      | `./.codex/skills/convert-sc-design-hblab` |
| Antigravity  | `~/.agent/skills/convert-sc-design-hblab`      | `./.agent/skills/convert-sc-design-hblab` |
| OpenCode     | `~/.config/opencode/skills/convert-sc-design-hblab` | `./.opencode/skills/convert-sc-design-hblab` |

## Thành phần được cài đặt

Skill này chỉ cài các tài nguyên cần thiết sau:

- `SKILL.md`
- `scripts/read_sheet.py`

Các tài nguyên này được lấy từ `skills/convert-sc-design-hblab/` trong repo.

Ngoài ra, skill trong repo còn bao gồm:

- `docs/troubleshooting.md`
- `examples/read-sheet-json.sh`
- `examples/read-sheet-table.sh`

## Vị trí xuất file

Thư mục cài skill chỉ dùng để chứa tài nguyên đóng gói. Kết quả đọc sheet phải được xuất vào `./docs` của workspace hiện tại.

Ví dụ:

```bash
mkdir -p ./docs
python3 <skill-dir>/scripts/read_sheet.py \
  --spreadsheet-id "<SPREADSHEET_ID>" \
  --gid "<GID>" \
  --format table \
  --output ./docs/<sheet-name>.md
```

Dùng `--sheet-name` khi muốn chỉ định tab theo tên. Dùng `--gid` khi đã biết Google Sheets tab id từ URL như `.../edit?gid=123#gid=123`. Nếu agent nhận được đầy đủ Google Sheets URL thì nó nên tự đọc `gid` từ URL đó và convert trực tiếp sheet tương ứng. Nếu truyền cả hai thì `--gid` sẽ được ưu tiên.

Script luôn trả về toàn bộ nội dung của sheet đã chọn theo đúng định dạng yêu cầu. Mặc định, nó không tóm tắt, không lấy mẫu, và không cắt bớt nội dung.

## Lưu ý khi sử dụng

- Cung cấp đầy đủ Google Sheets URL để agent có thể lấy `spreadsheet id` và tự đọc `gid` của sheet cần convert.
- Nếu URL đã mở đúng tab cần lấy thì có thể không cần ghi thêm tên sheet; `gid` trong URL là đủ để xác định sheet mục tiêu.
- Chỉ cần ghi tên sheet khi muốn nhấn mạnh lại tab mục tiêu hoặc khi link không thể hiện rõ tab cần xử lý.
- Nêu rõ rằng các sheet được reference cũng phải được đọc và nội dung của chúng phải được gộp trực tiếp vào file kết quả, thay vì để thành tham chiếu riêng.
- Yêu cầu xuất ra một file duy nhất trong `./docs`, ví dụ `./docs/sm-preview-site-recruitment-lp.md`.
- Nếu spreadsheet có nhiều tab liên quan, cần nói rõ là phải giữ nguyên toàn bộ nội dung nguồn và không được tóm tắt, trừ khi có yêu cầu khác.
