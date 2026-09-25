from nicegui import ui


@ui.page("/kurulum")
async def kurulum_sayfasi():
    # Sistem zaten kuruluysa giriş sayfasına yönlendir
    try:
        from merkez.veritabani import vt_getir
        havuz = await vt_getir()
        async with havuz.acquire() as db:
            sayi = await db.fetchval("SELECT COUNT(*) FROM kullanicilar;")
        if sayi > 0:
            ui.navigate.to("/giris")
            return
    except Exception:
        pass  # VT hazır değilse kurulum formunu göster

    # ── Sayfa düzeni ────────────────────────────────────────────────────────
    with ui.column().classes("w-full min-h-screen items-center justify-center bg-gray-50"):
        with ui.card().classes("w-[480px] shadow-lg"):
            with ui.column().classes("w-full gap-4 p-8"):

                ui.label("İlk Kurulum").classes("text-3xl font-bold text-center text-gray-800")
                ui.label("Sistem yöneticisi hesabını ve firma bilgilerini oluşturun.") \
                    .classes("text-center text-gray-500 text-sm")

                # ── Firma bilgileri ──────────────────────────────────────────
                ui.separator()
                ui.label("Firma Bilgileri").classes("font-semibold text-gray-700")

                firma_kodu_input = ui.input(
                    label="Firma Kodu",
                    placeholder="Örn: F001",
                    value="F001",
                ).props("outlined dense").classes("w-full")

                firma_adi_input = ui.input(
                    label="Firma Adı",
                    placeholder="Şirket Adı A.Ş.",
                ).props("outlined dense").classes("w-full")

                # ── Yönetici bilgileri ───────────────────────────────────────
                ui.separator()
                ui.label("Yönetici Bilgileri").classes("font-semibold text-gray-700")

                sicil_input = ui.input(
                    label="Sicil Numarası",
                    placeholder="Örn: ADM001",
                ).props("outlined dense").classes("w-full")

                with ui.row().classes("w-full gap-2"):
                    ad_input = ui.input(
                        label="Ad",
                        placeholder="Adınız",
                    ).props("outlined dense").classes("flex-1")

                    soyad_input = ui.input(
                        label="Soyad",
                        placeholder="Soyadınız",
                    ).props("outlined dense").classes("flex-1")

                email_input = ui.input(
                    label="E-Posta",
                    placeholder="admin@firma.com",
                ).props("outlined dense").classes("w-full")

                parola_input = ui.input(
                    label="Şifre",
                    placeholder="Güçlü bir şifre giriniz",
                    password=True,
                    password_toggle_button=True,
                ).props("outlined dense").classes("w-full")

                hata_etiketi = ui.label("").classes("text-red-500 text-sm min-h-4")

                # ── Kurulum işlemi ───────────────────────────────────────────
                async def kurulum_islemi():
                    hata_etiketi.set_text("")
                    alanlar = [
                        firma_kodu_input.value, firma_adi_input.value,
                        sicil_input.value, ad_input.value, soyad_input.value,
                        email_input.value, parola_input.value,
                    ]
                    if not all(a.strip() for a in alanlar):
                        hata_etiketi.set_text("Lütfen tüm alanları eksiksiz doldurunuz.")
                        return

                    from merkez.servisler.kurulum import ilk_kurulumu_yap
                    from merkez.semalar.kurulum import KurulumGirisi

                    giris_verisi = KurulumGirisi(
                        sicil=sicil_input.value.strip(),
                        ad=ad_input.value.strip(),
                        soyad=soyad_input.value.strip(),
                        email=email_input.value.strip(),
                        parola=parola_input.value,
                        firma_kodu=firma_kodu_input.value.strip(),
                        firma_adi=firma_adi_input.value.strip(),
                    )

                    try:
                        await ilk_kurulumu_yap(giris_verisi)
                        ui.notify("Kurulum tamamlandı! Giriş sayfasına yönlendiriliyorsunuz.", type="positive")
                        ui.navigate.to("/giris")
                    except ValueError as hata:
                        hata_etiketi.set_text(str(hata))
                    except Exception:
                        hata_etiketi.set_text("Kurulum sırasında bir hata oluştu. Veritabanı bağlantısını kontrol edin.")

                ui.button(
                    "Kurulumu Tamamla",
                    on_click=kurulum_islemi,
                ).props("color=primary unelevated").classes("w-full")
