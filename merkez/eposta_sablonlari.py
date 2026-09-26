from dataclasses import dataclass
from datetime import datetime
from html import escape
from merkez.sabitler import UYGULAMA_ADI

_ANA_RENK = "#5898d4"


@dataclass(frozen=True)
class Eposta:
    konu: str
    metin: str
    html: str


def _sablon(baslik: str, icerik_html: str) -> str:
    # E-posta istemcileri harici stil dosyası desteklemediği için stiller satır içi (inline) yazılır.
    return f"""<!DOCTYPE html>
<html lang="tr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(baslik)}</title></head>
<body style="margin:0;padding:0;background-color:#f3f5f8;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f3f5f8;padding:32px 12px;font-family:'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <tr><td align="center">
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;background-color:#ffffff;border:1px solid #e3e8ee;border-radius:12px;">
      <tr><td style="padding:22px 32px;background-color:{_ANA_RENK};border-radius:12px 12px 0 0;color:#ffffff;font-size:18px;font-weight:600;">
        {escape(UYGULAMA_ADI)}
      </td></tr>
      <tr><td style="padding:32px;color:#374151;font-size:15px;line-height:1.6;">
        {icerik_html}
      </td></tr>
      <tr><td style="padding:16px 32px;background-color:#f9fafb;border-top:1px solid #eef1f4;border-radius:0 0 12px 12px;color:#9ca3af;font-size:12px;line-height:1.5;">
        Bu e-posta otomatik olarak gönderilmiştir, lütfen yanıtlamayın.
      </td></tr>
    </table>
    <p style="margin:16px 0 0;color:#9ca3af;font-size:12px;">&copy; {datetime.now().year} {escape(UYGULAMA_ADI)}</p>
  </td></tr>
</table>
</body>
</html>"""


def sifre_sifirlama_epostasi(ad_soyad: str, baglanti: str, gecerlilik_dakika: int, talep_ip: str | None) -> Eposta:
    konu = "Şifre Sıfırlama Talebi"
    zaman = datetime.now().strftime("%d.%m.%Y %H:%M")
    talep_bilgisi = f"{zaman}" + (f" · IP: {talep_ip}" if talep_ip else "")

    metin = (
        f"Merhaba {ad_soyad},\n\n"
        f"Hesabınız için bir şifre sıfırlama talebi aldık. Yeni şifrenizi belirlemek için "
        f"aşağıdaki bağlantıyı açın. Bağlantı {gecerlilik_dakika} dakika geçerlidir ve yalnızca bir kez kullanılabilir.\n\n"
        f"{baglanti}\n\n"
        f"Talep: {talep_bilgisi}\n\n"
        f"Bu talebi siz yapmadıysanız bu e-postayı dikkate almayın; şifreniz değişmez."
    )

    link = escape(baglanti, quote=True)
    icerik = f"""
        <h1 style="margin:0 0 16px;font-size:22px;color:#111827;">Şifrenizi sıfırlayın</h1>
        <p style="margin:0 0 12px;">Merhaba <strong>{escape(ad_soyad)}</strong>,</p>
        <p style="margin:0 0 24px;">Hesabınız için bir şifre sıfırlama talebi aldık. Yeni şifrenizi belirlemek için aşağıdaki butona tıklayın.</p>
        <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 24px;">
          <tr><td style="border-radius:8px;background-color:{_ANA_RENK};">
            <a href="{link}" style="display:inline-block;padding:13px 30px;color:#ffffff;font-size:15px;font-weight:600;text-decoration:none;">Şifremi Sıfırla</a>
          </td></tr>
        </table>
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:0 0 24px;background-color:#fff8e6;border:1px solid #fde7b0;border-radius:8px;">
          <tr><td style="padding:12px 16px;color:#8a6116;font-size:13px;">
            Bağlantı <strong>{gecerlilik_dakika} dakika</strong> geçerlidir ve yalnızca bir kez kullanılabilir.
          </td></tr>
        </table>
        <p style="margin:0 0 6px;color:#6b7280;font-size:13px;">Buton çalışmazsa bu bağlantıyı tarayıcınıza yapıştırın:</p>
        <p style="margin:0 0 24px;font-size:13px;word-break:break-all;"><a href="{link}" style="color:{_ANA_RENK};">{escape(baglanti)}</a></p>
        <hr style="border:none;border-top:1px solid #eef1f4;margin:0 0 16px;">
        <p style="margin:0 0 4px;color:#6b7280;font-size:12px;">Talep bilgisi: {escape(talep_bilgisi)}</p>
        <p style="margin:0;color:#6b7280;font-size:12px;">Bu talebi siz yapmadıysanız bu e-postayı dikkate almayın; şifreniz değişmez.</p>
    """
    return Eposta(konu=konu, metin=metin, html=_sablon(konu, icerik))