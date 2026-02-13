import os
import smtplib
import getpass
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def attach_file(msg, file_path, filename):
    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)


def main():
    sender_email = input("Masukkan email Anda (Gmail): ").strip()
    sender_password = getpass.getpass("Masukkan App Password Gmail: ").strip()
    sender_password = "".join(sender_password.split())
    if len(sender_password) != 16:
        print(
            "[WARN] App Password biasanya 16 karakter. "
            "Pastikan kamu pakai App Password terbaru dari Google."
        )
    recipient_email = input("Masukkan email cewe Anda: ").strip()

    surprise_url = input(
        "Link kejutan (opsional, contoh GitHub Pages/Drive, Enter jika tidak ada): "
    ).strip()

    subject = "For You"
    plain_body = (
        "Halo honey,\n\n"
        "Aku kirim kejutan kecil buat kamu.\n"
        "Kalau tombol tidak bisa diklik, buka lampiran valentine.html.\n\n"
        "I love you"
    )

    msg = MIMEMultipart("related")
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject

    alternative = MIMEMultipart("alternative")
    msg.attach(alternative)
    alternative.attach(MIMEText(plain_body, "plain", "utf-8"))

    button_html = ""
    if surprise_url:
        button_html = f"""
        <p style=\"margin:24px 0;\">
          <a href=\"{surprise_url}\"
             style=\"display:inline-block;padding:14px 24px;background:#e63946;color:#fff;text-decoration:none;border-radius:10px;font-weight:bold;\">
            Buka Kejutan
          </a>
        </p>
        """

    html_body = f"""
    <html>
      <body style=\"margin:0;padding:24px;background:#fff5f7;font-family:Arial,sans-serif;color:#222;\">
        <div style=\"max-width:560px;margin:0 auto;background:#ffffff;border-radius:14px;padding:24px;border:1px solid #ffd6de;\">
          <h2 style=\"margin:0 0 10px;color:#d62839;\">For You</h2>
          <p style=\"margin:0 0 16px;\">I love you, honey.</p>
          <img src=\"cid:photo_cid\" alt=\"Our photo\" style=\"width:100%;max-width:420px;border-radius:12px;border:3px solid #ffd6de;display:block;margin:0 auto;\" />
          {button_html}
          <p style=\"margin-top:18px;color:#555;\">Kalau tombol tidak jalan, buka lampiran <b>valentine.html</b>.</p>
        </div>
      </body>
    </html>
    """
    alternative.attach(MIMEText(html_body, "html", "utf-8"))

    base_dir = os.path.dirname(__file__)

    image_path = os.path.join(base_dir, "pict.jpeg")
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            image = MIMEImage(img_file.read())
        image.add_header("Content-ID", "<photo_cid>")
        image.add_header("Content-Disposition", "inline", filename="pict.jpeg")
        msg.attach(image)
        print("[OK] pict.jpeg di-embed ke body email")
    else:
        print("[WARN] pict.jpeg tidak ditemukan")

    html_attachment_path = os.path.join(base_dir, "valentine.html")
    if os.path.exists(html_attachment_path):
        attach_file(msg, html_attachment_path, "valentine.html")
        print("[OK] valentine.html dilampirkan")
    else:
        print("[WARN] valentine.html tidak ditemukan")

    try:
        print("\nMengirim email...")
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("[OK] Email berhasil dikirim")
    except Exception as exc:
        print(f"[ERROR] Gagal kirim email: {exc}")
        print("Pastikan Gmail pakai App Password, bukan password biasa.")


if __name__ == "__main__":
    main()
