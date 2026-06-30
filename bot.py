import pytz
from datetime import datetime
from discord.ext import tasks
import time
import asyncio
import random
import json
from keep_alive import keep_alive
import discord
from discord.ext import commands
import random
import json
import os
from dotenv import load_dotenv

KELIME_HAVUZU = ["KİTAP", "KALEM", "SEVGİ", "BARIŞ", "HAYAT", "BİLGİ", "ZAMAN", "DOĞA", "DENİZ", "GÜNEŞ", "ÇİÇEK", "ORMAN", "MÜZİK", "SANAT", "ASLAN", "KARTAL"]

# Gizli .env dosyasını sisteme yüklüyoruz
load_dotenv()
import time

# İzinleri (Intents) KODUN İÇİNDE de aktif etmeliyiz:
intents = discord.Intents.default()
intents.message_content = True # Botun mesajları okuması için en önemli izin bu!
intents.members = True         # YENİ EKLENEN: Botun sunucudaki üyeleri görüp rol verebilmesi için!

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'Tebrikler! {bot.user} başarıyla çalışıyor ve sunucuya hazır.')
    # Bota oyun oynuyor durumu ekliyoruz:
    await bot.change_presence(activity=discord.Game(name="Berkerin hayalleri ile oynuyor!"))

# İlk komutumuz:
@bot.command()
async def selam(ctx):
    await ctx.send(f'Merhaba {ctx.author.name}! Ben hazırım.')

# Rastgele oyun seçme komutumuz (100 Oyunluk Dev Liste):
@bot.command()
async def oyunseç(ctx):
    oyunlar = [
        "League of Legends", "Red Dead Redemption 2", "EA SPORTS FC 26", "Mobile Legends: Bang Bang", "Clash Royale",
        "Ghost of Tsushima", "Roblox", "Hero Siege", "Plague Inc.", "Minecraft",
        "Grand Theft Auto V", "Counter-Strike 2", "Valorant", "Dota 2", "Apex Legends",
        "Fortnite", "Call of Duty: Warzone", "Overwatch 2", "Cyberpunk 2077", "The Witcher 3: Wild Hunt",
        "Elden Ring", "Baldur's Gate 3", "Helldivers 2", "Palworld", "Rocket League",
        "Tom Clancy's Rainbow Six Siege", "Destiny 2", "World of Warcraft", "Final Fantasy XIV", "Genshin Impact",
        "Honkai: Star Rail", "PUBG: Battlegrounds", "Rust", "Terraria", "Stardew Valley",
        "Hollow Knight", "Hades", "Dead Cells", "Celeste", "Among Us",
        "Fall Guys", "The Sims 4", "Super Mario Odyssey", "The Legend of Zelda: Breath of the Wild", "God of War",
        "Marvel's Spider-Man Remastered", "Horizon Zero Dawn", "The Last of Us Part I", "Bloodborne", "Dark Souls III",
        "Sekiro: Shadows Die Twice", "Persona 5 Royal", "Resident Evil 4 Remake", "Dead by Daylight", "Left 4 Dead 2",
        "Phasmophobia", "Lethal Company", "Sea of Thieves", "No Man's Sky", "Halo Infinite",
        "Forza Horizon 5", "Microsoft Flight Simulator", "Assassin's Creed Valhalla", "Far Cry 6", "Fallout 4",
        "The Elder Scrolls V: Skyrim", "DOOM Eternal", "Half-Life 2", "Portal 2", "Garry's Mod",
        "Team Fortress 2", "Warframe", "Path of Exile", "Diablo IV", "Smite",
        "Paladins", "ARK: Survival Evolved", "DayZ", "Escape from Tarkov", "Hunt: Showdown",
        "Tekken 8", "Street Fighter 6", "Mortal Kombat 1", "Super Smash Bros. Ultimate", "Mario Kart 8 Deluxe",
        "Splatoon 3", "Monster Hunter: World", "Cities: Skylines", "Sid Meier's Civilization VI", "Crusader Kings III",
        "Hearts of Iron IV", "Age of Empires II: Definitive Edition", "StarCraft II", "osu!", "Beat Saber",
        "Geometry Dash", "World of Tanks", "War Thunder", "EVE Online", "Old School RuneScape"
    ]
    secilen_oyun = random.choice(oyunlar)
    await ctx.send(f'🎮 Yüzlerce oyun arasından senin için bunu seçtim. Bence şu an bunu oynamalısın: **{secilen_oyun}**')

# Mesaj silme (temizleme) komutu:
@bot.command()
async def sil(ctx, miktar: int):
    # Komutu yazdığımız mesajı da saydığı için miktara 1 ekliyoruz
    await ctx.channel.purge(limit=miktar + 1)
    
    # Silme işleminden sonra bilgi mesajı gönderiyoruz (ve o mesaj da 5 saniye sonra kendi kendini siliyor)
    await ctx.send(f'🧹 Başarıyla **{miktar}** adet mesaj silindi!', delete_after=5)

 # Profesyonel görünümlü (Embed) profil kartı komutu:
@bot.command()
async def profil(ctx):
    # Embed mesajımızın ana iskeletini, rengini ve başlığını ayarlıyoruz
    embed = discord.Embed(
        title=f"Kullanıcı Bilgi Kartı",
        description="İşte Discord profil bilgilerin:",
        color=discord.Color.random() # Her seferinde rastgele bir renk seçer!
    )
    
    # Karta küçük bilgi kutucukları (field) ekliyoruz
    embed.add_field(name="Kullanıcı Adı", value=ctx.author.name, inline=True)
    embed.add_field(name="Hesap ID", value=ctx.author.id, inline=True)
    
    # Eğer kullanıcının profil fotoğrafı varsa onu sağ üstte gösteriyoruz
    if ctx.author.avatar:
        embed.set_thumbnail(url=ctx.author.avatar.url)
    else:
        embed.set_thumbnail(url=ctx.author.default_avatar.url)

    # Hazırladığımız bu şık kartı kanala gönderiyoruz
    await ctx.send(embed=embed)

       # Botun bağlantı hızını (Ping) ölçme komutu:
@bot.command()
async def ping(ctx):
    # bot.latency bize saniye cinsinden gecikmeyi verir, onu 1000 ile çarpıp milisaniyeye (ms) çeviriyoruz
    gecikme = round(bot.latency * 1000)
    await ctx.send(f'🏓 Pong! Şu anki gecikme sürem: **{gecikme}ms**')

# Sihirli Küre komutu (kullanıcıdan uzun bir soru cümlesi alma):
@bot.command(aliases=['sor', 'küre'])
async def sihirli_kure(ctx, *, soru):
    # *, soru kısmı, komuttan sonra yazılan BÜTÜN kelimeleri tek bir cümle olarak almasını sağlar
    cevaplar = [
        "Kesinlikle evet.", "Görünüşe göre öyle.", "Buna şüphe yok.",
        "Şimdilik buna cevap veremem, kafam biraz karışık.", "Daha sonra tekrar sor.",
        "Buna pek güvenme.", "Kaynaklarım 'kesinlikle hayır' diyor.", "Durum çok şüpheli."
    ]
    secilen_cevap = random.choice(cevaplar)
    
    # Kullanıcının sorusunu ve botun cevabını aynı mesajda gönderiyoruz
    await ctx.send(f'🎱 **Senin Sorun:** {soru}\n🔮 **Kürenin Cevabı:** {secilen_cevap}')

# Gelişmiş ve çeşitli sarılma komutu (Türkçe karakterli):
@bot.command()
async def sarıl(ctx, uye: discord.Member):
    # Farklı etkileşim mesajlarından oluşan bir liste hazırlıyoruz
    mesajlar = [
        f'🤗 {ctx.author.mention}, {uye.mention} adlı kullanıcıya kocaman sarıldı!',
        f'💖 {ctx.author.mention}, {uye.mention} kişisine sevgi dolu bir kucaklama gönderdi!',
        f'🫂 {ctx.author.mention} koşarak geldi ve {uye.mention} kullanıcısına sımsıkı sarıldı!',
        f'✨ {ctx.author.mention}, {uye.mention} ile dostça kucaklaştı.',
        f'🐻 {ctx.author.mention}, {uye.mention} kişisine dev bir ayı sarılması yaptı!'
    ]
    
    # Listeden rastgele bir mesaj seçtirip gönderiyoruz
    secilen_mesaj = random.choice(mesajlar)
    await ctx.send(secilen_mesaj)

# Hata yakalama (Eğer etiketlemeyi unutursa):
@sarıl.error
async def sarıl_hata(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Lütfen sarılmak için birini etiketle! Örnek: `!sarıl @KullaniciAdi`")
    
# Sohbeti dinleme, mesaj sayacı, kanal takibi ve ZORLAŞTIRILMIŞ SEVİYE SİSTEMİ
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    dosya_adi = "veriler.json"
    
    if not os.path.exists(dosya_adi):
        with open(dosya_adi, "w", encoding="utf-8") as f:
            json.dump({}, f)
            
    with open(dosya_adi, "r", encoding="utf-8") as f:
        kullanicilar = json.load(f)
        
    kullanici_id = str(message.author.id)
    kanal_adi = message.channel.name
    
    if kullanici_id not in kullanicilar:
        kullanicilar[kullanici_id] = {
            "mesaj_sayisi": 1, 
            "sesli_suresi": 0, 
            "yayin_suresi": 0,
            "mesaj_kanallari": {kanal_adi: 1},
            "ses_kanallari": {},
            "xp": random.randint(10, 20), # DÜŞÜRÜLDÜ: İlk mesajında 10-20 arası XP ile başlar
            "seviye": 1
        }
    else:
        kullanicilar[kullanici_id]["mesaj_sayisi"] += 1
        
        if "mesaj_kanallari" not in kullanicilar[kullanici_id]:
            kullanicilar[kullanici_id]["mesaj_kanallari"] = {}
            
        if kanal_adi not in kullanicilar[kullanici_id]["mesaj_kanallari"]:
            kullanicilar[kullanici_id]["mesaj_kanallari"][kanal_adi] = 1
        else:
            kullanicilar[kullanici_id]["mesaj_kanallari"][kanal_adi] += 1
            
        if "xp" not in kullanicilar[kullanici_id]:
            kullanicilar[kullanici_id]["xp"] = 0
            kullanicilar[kullanici_id]["seviye"] = 1
            
        # DÜŞÜRÜLDÜ: Her mesaja 10 ile 20 arası rastgele XP veriyoruz
        kazanilan_xp = random.randint(10, 20)
        kullanicilar[kullanici_id]["xp"] += kazanilan_xp
        
        mevcut_seviye = kullanicilar[kullanici_id]["seviye"]
        mevcut_xp = kullanicilar[kullanici_id]["xp"]
        
        # ZORLAŞTIRILDI: Seviye atlama sınırı artık Mevcut Seviye x 300
        hedef_xp = mevcut_seviye * 300
        
        if mevcut_xp >= hedef_xp:
            kullanicilar[kullanici_id]["seviye"] += 1
            # Seviye atladığında artan XP'yi silmiyoruz, bir sonraki seviyeye devrediyoruz (Daha adil bir sistem)
            kullanicilar[kullanici_id]["xp"] = mevcut_xp - hedef_xp 
            yeni_seviye = kullanicilar[kullanici_id]["seviye"]
            
            await message.channel.send(f"🎉 Tebrikler {message.author.mention}! Yeni bir seviyeye ulaştın: **{yeni_seviye}. Seviye** 🚀")

    with open(dosya_adi, "w", encoding="utf-8") as f:
        json.dump(kullanicilar, f, indent=4)
        
    if message.content.lower() == "sa":
        await message.channel.send(f'Aleyküm Selam {message.author.mention}, hoş geldin! 🌟')

    await bot.process_commands(message)
    # Oylama (Anket) komutu:
@bot.command()
async def oylama(ctx, *, konu):
    # Oylama için şık bir Embed kartı hazırlıyoruz
    embed = discord.Embed(
        title="📊 Yeni Bir Oylama Var!",
        description=f"**Konu:** {konu}",
        color=discord.Color.blue()
    )
    embed.set_footer(text=f"Oylamayı başlatan: {ctx.author.name}")
    
    # Hazırladığımız bu kartı kanala gönderip "anket_mesaji" adında bir değişkene kaydediyoruz
    anket_mesaji = await ctx.send(embed=embed)
    
    # Botun bu mesaja otomatik olarak Evet ve Hayır emojilerini eklemesini sağlıyoruz
    await anket_mesaji.add_reaction("✅")
    await anket_mesaji.add_reaction("❌")

# Günün Finali: Avatar (Profil Fotoğrafı) gösterme komutu:
@bot.command()
async def avatar(ctx, uye: discord.Member = None):
    # Eğer komutu yazan kişi kimseyi etiketlemezse, kendi avatarını gösteririz
    if uye is None:
        uye = ctx.author
        
    # Avatar için şık bir Embed çerçevesi oluşturuyoruz
    embed = discord.Embed(
        title=f"{uye.name} adlı kullanıcının profil fotoğrafı",
        color=discord.Color.purple()
    )
    
    # Kullanıcının avatarını yüksek çözünürlükte embed'in içine ekliyoruz
    if uye.avatar:
        embed.set_image(url=uye.avatar.url)
    else:
        # Eğer kullanıcının özel bir fotoğrafı yoksa Discord'un varsayılan fotoğrafını çeker
        embed.set_image(url=uye.default_avatar.url)
        
    await ctx.send(embed=embed)

    # Sürpriz Final: Zar Atma Komutu
@bot.command()
async def zar(ctx):
    # 1 ile 6 arasında rastgele bir tam sayı seçiyoruz
    zar_sonucu = random.randint(1, 6)
    
    # Sonuca göre özel mesajlar ayarlıyoruz
    if zar_sonucu == 6:
        await ctx.send(f'🎲 Şanslı günündesin {ctx.author.mention}! Zarın **6** geldi. Harika bir atış!')
    elif zar_sonucu == 1:
        await ctx.send(f'🎲 Tüh {ctx.author.mention}... Zarın **1** geldi. Belki de bugün senin günün değildir.')
    else:
        await ctx.send(f'🎲 {ctx.author.mention}, zarları yuvarladın ve **{zar_sonucu}** geldi.')
        
        # Giriş zamanlarını tutacağımız geçici hafıza
sesli_baslangiclar = {}

sesli_baslangiclar = {}
yayin_baslangiclar = {}

@bot.event
async def on_voice_state_update(member, before, after):
    # --- 1. KISIM: SES KANALI GİRİŞ/ÇIKIŞ TAKİBİ ---
    if before.channel is None and after.channel is not None:
        sesli_baslangiclar[member.id] = time.time()
        
    elif before.channel is not None and after.channel is None:
        if member.id in sesli_baslangiclar:
            baslangic = sesli_baslangiclar.pop(member.id)
            gecen_sure = int(time.time() - baslangic)
            ses_kanal_adi = before.channel.name # Ayrıldığı ses kanalının adı
            
            try:
                with open("veriler.json", "r") as f:
                    kullanicilar = json.load(f)
            except FileNotFoundError:
                kullanicilar = {}
            
            kullanici_id = str(member.id)
            
            if kullanici_id not in kullanicilar:
                kullanicilar[kullanici_id] = {
                    "mesaj_sayisi": 0, 
                    "sesli_suresi": gecen_sure, 
                    "yayin_suresi": 0,
                    "mesaj_kanallari": {},
                    "ses_kanallari": {ses_kanal_adi: gecen_sure}
                }
            else:
                if "sesli_suresi" not in kullanicilar[kullanici_id]:
                    kullanicilar[kullanici_id]["sesli_suresi"] = 0
                kullanicilar[kullanici_id]["sesli_suresi"] += gecen_sure
                
                # 'ses_kanallari' alt listesi kontrolü
                if "ses_kanallari" not in kullanicilar[kullanici_id]:
                    kullanicilar[kullanici_id]["ses_kanallari"] = {}
                    
                if ses_kanal_adi not in kullanicilar[kullanici_id]["ses_kanallari"]:
                    kullanicilar[kullanici_id]["ses_kanallari"][ses_kanal_adi] = gecen_sure
                else:
                    kullanicilar[kullanici_id]["ses_kanallari"][ses_kanal_adi] += gecen_sure
            
            with open("veriler.json", "w") as f:
                json.dump(kullanicilar, f, indent=4)

    # --- 2. KISIM: YAYIN TAKİBİ ---
    if not before.self_stream and after.self_stream:
        yayin_baslangiclar[member.id] = time.time()
    elif before.self_stream and not after.self_stream:
        if member.id in yayin_baslangiclar:
            yayin_bas = yayin_baslangiclar.pop(member.id)
            yayin_sure = int(time.time() - yayin_bas)
            
            with open("veriler.json", "r") as f:
                kullanicilar = json.load(f)
                
            kullanici_id = str(member.id)
            if kullanici_id not in kullanicilar:
                kullanicilar[kullanici_id] = {"mesaj_sayisi": 0, "sesli_suresi": 0, "yayin_suresi": yayin_sure, "mesaj_kanallari": {}, "ses_kanallari": {}}
            else:
                if "yayin_suresi" not in kullanicilar[kullanici_id]:
                    kullanicilar[kullanici_id]["yayin_suresi"] = 0
                kullanicilar[kullanici_id]["yayin_suresi"] += yayin_sure
                
            with open("veriler.json", "w") as f:
                json.dump(kullanicilar, f, indent=4)
                # YENİ NESİL İSTATİSTİK KOMUTU (Kanal ve Yayın Takibi Dahil)

# YENİ NESİL İSTATİSTİK KOMUTU (Başkalarının istatistiğini görme eklendi)
@bot.command()
async def istatistik(ctx, uye: discord.Member = None):
    # Eğer komutu yazarken yanına birini etiketlemediyse, hedef kendisi (ctx.author) olsun
    hedef_uye = uye if uye else ctx.author
    
    try:
        with open("veriler.json", "r", encoding="utf-8") as f:
            kullanicilar = json.load(f)
            
        kullanici_id = str(hedef_uye.id)
        
        if kullanici_id in kullanicilar:
            veri = kullanicilar[kullanici_id]
            mesaj_sayisi = veri.get("mesaj_sayisi", 0)
            sesli_suresi = veri.get("sesli_suresi", 0)
            yayin_suresi = veri.get("yayin_suresi", 0)
            seviye = veri.get("seviye", 1)
            xp = veri.get("xp", 0)
            hedef_xp = seviye * 300
            
            yuzde = int((xp / hedef_xp) * 10) if hedef_xp > 0 else 0
            ilerleme_bari = "🟩" * yuzde + "⬛" * (10 - yuzde)
            
            def sure_hesapla(saniye):
                if saniye == 0: return "0 sn"
                dk = saniye // 60
                sn = saniye % 60
                sa = dk // 60
                dk = dk % 60
                metin = ""
                if sa > 0: metin += f"{sa} saat "
                if dk > 0 or sa > 0: metin += f"{dk} dk "
                metin += f"{sn} sn"
                return metin

            mesaj_kanallari = veri.get("mesaj_kanallari", {})
            yazi_dokumu = ""
            if mesaj_kanallari:
                sirali_yazi = sorted(mesaj_kanallari.items(), key=lambda x: x[1], reverse=True)
                for kanal, sayi in sirali_yazi:
                    yazi_dokumu += f"• **{kanal}**: `{sayi} mesaj`\n"
            else:
                yazi_dokumu = "Henüz mesaj geçmişi yok."

            ses_kanallari = veri.get("ses_kanallari", {})
            ses_dokumu = ""
            if ses_kanallari:
                sirali_ses = sorted(ses_kanallari.items(), key=lambda x: x[1], reverse=True)
                for kanal, saniye in sirali_ses:
                    ses_dokumu += f"• **{kanal}**: `{sure_hesapla(saniye)}`\n"
            else:
                ses_dokumu = "Henüz sesli verisi yok."

            embed = discord.Embed(
                title=f"📊 {hedef_uye.name} - Sunucu Analizi",
                color=discord.Color.gold()
            )
            
            embed.add_field(name="⭐ Seviye", value=f"**{seviye}. Seviye**", inline=True)
            embed.add_field(name="✨ Tecrübe (XP)", value=f"`{xp} / {hedef_xp} XP`", inline=True)
            embed.add_field(name="📈 İlerleme", value=f"{ilerleme_bari}", inline=False)
            
            embed.add_field(name="\u200b", value="\u200b", inline=False)
            
            embed.add_field(name=f"💬 Toplam Mesaj: {mesaj_sayisi}", value=yazi_dokumu, inline=False)
            embed.add_field(name=f"🔊 Toplam Sesli Süre: {sure_hesapla(sesli_suresi)}", value=ses_dokumu, inline=False)
            embed.add_field(name="🎮 Toplam Yayın Süresi", value=f"**{sure_hesapla(yayin_suresi)}**", inline=False)
            
            if hedef_uye.avatar:
                embed.set_thumbnail(url=hedef_uye.avatar.url)
            else:
                embed.set_thumbnail(url=hedef_uye.default_avatar.url)
                
            await ctx.send(embed=embed)
        else:
            # Hedef kişi sen değilsen ve veri yoksa farklı mesaj ver
            if uye:
                await ctx.send(f"Veritabanında **{hedef_uye.name}** adlı kullanıcının henüz bir kaydı yok.")
            else:
                await ctx.send("Veritabanında henüz kaydın yok. Biraz mesaj yazmayı veya sesliye girmeyi dene!")
            
    except FileNotFoundError:
        await ctx.send("Henüz bir veritabanı oluşturulmadı.")
        
# SUNUCU LİDERLİK TABLOSU KOMUTU (GÜNCELLENDİ - BİLİNMEYEN ÜYE HATASI ÇÖZÜLDÜ)
@bot.command(aliases=['top', 'liderlik'])
async def siralama(ctx):
    try:
        with open("veriler.json", "r", encoding="utf-8") as f:
            kullanicilar = json.load(f)

        if not kullanicilar:
            return await ctx.send("Henüz sunucuda yeterli veri yok.")

        mesaj_siralamasi = sorted(kullanicilar.items(), key=lambda x: x[1].get("mesaj_sayisi", 0), reverse=True)
        ses_siralamasi = sorted(kullanicilar.items(), key=lambda x: x[1].get("sesli_suresi", 0), reverse=True)

        embed = discord.Embed(
            title="🏆 Sunucu Liderlik Tablosu",
            description="Sunucumuzun en aktif ve efsanevi üyeleri!",
            color=discord.Color.brand_red()
        )

        # --- MESAJ ŞAMPİYONLARI ---
        mesaj_metni = ""
        for i, (k_id, veri) in enumerate(mesaj_siralamasi[:3], 1):
            try:
                # Bota kullanıcıyı Discord veritabanından zorla bulduruyoruz
                uye = await bot.fetch_user(int(k_id))
                isim = uye.name
            except:
                isim = "Bilinmeyen Üye"
                
            mesaj_metni += f"**{i}.** {isim} - `{veri.get('mesaj_sayisi', 0)} mesaj`\n"
        
        if mesaj_metni:
            embed.add_field(name="💬 En Çok Mesaj Yazanlar", value=mesaj_metni, inline=False)

        # --- SES ŞAMPİYONLARI ---
        ses_metni = ""
        for i, (k_id, veri) in enumerate(ses_siralamasi[:3], 1):
            try:
                uye = await bot.fetch_user(int(k_id))
                isim = uye.name
            except:
                isim = "Bilinmeyen Üye"
            
            saniye = veri.get("sesli_suresi", 0)
            dk = saniye // 60
            sa = dk // 60
            dk = dk % 60
            sure_str = f"{sa}s {dk}dk" if sa > 0 else f"{dk}dk {saniye%60}sn"

            ses_metni += f"**{i}.** {isim} - `{sure_str}`\n"

        if ses_metni:
            embed.add_field(name="🔊 Seste En Çok Kalanlar", value=ses_metni, inline=False)

        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        await ctx.send(embed=embed)

    except FileNotFoundError:
        await ctx.send("Henüz bir veritabanı oluşturulmadı.")

# YETKİ AYARLI VE GİZLİ KANALLI PROFESYONEL SUNUCU KURMA KOMUTU (NİHAİ SÜRÜM)
@bot.command()
@commands.has_permissions(administrator=True)
async def sunucukur(ctx):
    await ctx.send("🛠️ Gelişmiş yetki ayarlarına sahip sunucu altyapısı inşa ediliyor... Lütfen bekle!")

    # --- 1. ROL ÇEŞİTLİLİĞİ, YETKİ VE GÖRÜNÜM KURULUMU ---
    # Moderatörler için özel yetkiler (Mesaj silme, üye atma, vb.)
    mod_yetkisi = discord.Permissions(manage_messages=True, kick_members=True, moderate_members=True)
    standart_yetki = discord.Permissions() # Sadece mesaj yazma/okuma
    
    # Liste yapısı: (Rol Adı, Renk, Sağda Ayrı Gösterilsin mi?, Yetkileri)
    rol_listesi = [
        ("👑 Sunucu Sahibi", discord.Color.gold(), True, discord.Permissions.all()),
        ("🤖 Asistan Bot", discord.Color.blue(), True, discord.Permissions.all()),
        ("🛡️ Moderatör", discord.Color.dark_green(), True, mod_yetkisi),
        ("💎 VIP / Efsanevi Üye", discord.Color.purple(), True, standart_yetki),
        ("💻 Geliştirici & Yazılımcı", discord.Color.dark_theme(), False, standart_yetki),
        ("📚 Filozof & Kitap Kurdu", discord.Color.dark_orange(), False, standart_yetki),
        ("🗣️ English B1+ Club", discord.Color.light_grey(), False, standart_yetki),
        ("🧠 Trivia & Kelime Ustası", discord.Color.teal(), False, standart_yetki),
        ("🏃‍♂️ Fitness & Aktif Yaşam", discord.Color.green(), False, standart_yetki),
        ("🤠 Vahşi Batı Efsanesi", discord.Color.dark_red(), False, standart_yetki),
        ("⚽ Yeşil Saha Ustası", discord.Color.teal(), False, standart_yetki),
        ("⚔️ Vadi Savaşçısı", discord.Color.blue(), False, standart_yetki),
        ("👤 Üye", discord.Color.default(), True, standart_yetki) # Üyeler ayrı gözüksün
    ]
    
    olusturulan_roller = {}
    for ad, renk, ayri_goster, yetki in rol_listesi:
        rol = discord.utils.get(ctx.guild.roles, name=ad)
        if not rol:
            # Rol yoksa tüm bu özelliklerle sıfırdan oluştur
            rol = await ctx.guild.create_role(name=ad, color=renk, hoist=ayri_goster, permissions=yetki)
        else:
            # Rol zaten varsa yetkilerini ve görünümünü güncelle
            await rol.edit(color=renk, hoist=ayri_goster, permissions=yetki)
        olusturulan_roller[ad] = rol

    # İzinler için rolleri hafızaya alıyoruz
    everyone = ctx.guild.default_role
    mod_rolu = olusturulan_roller.get("🛡️ Moderatör")
    yazilim_rolu = olusturulan_roller.get("💻 Geliştirici & Yazılımcı")
    ingilizce_rolu = olusturulan_roller.get("🗣️ English B1+ Club")
    kitap_rolu = olusturulan_roller.get("📚 Filozof & Kitap Kurdu")
    rdr2_rolu = olusturulan_roller.get("🤠 Vahşi Batı Efsanesi")
    fc_rolu = olusturulan_roller.get("⚽ Yeşil Saha Ustası")
    lol_rolu = olusturulan_roller.get("⚔️ Vadi Savaşçısı")
    trivia_rolu = olusturulan_roller.get("🧠 Trivia & Kelime Ustası")

    # Pratik bir izin fonksiyonu (Sadece belirtilen role kanalı gösterir, diğerlerine gizler)
    def sadece_bu_rol_gorsun(ozel_rol):
        return {
            everyone: discord.PermissionOverwrite(view_channel=False),
            ozel_rol: discord.PermissionOverwrite(view_channel=True, send_messages=True)
        }

    # --- 2. KATEGORİ VE KANALLARIN İNŞASI ---

    # 📌 BİLGİLENDİRME (Herkes okur, sadece Modlar ve Yönetim yazar)
    izin_duyuru = {
        everyone: discord.PermissionOverwrite(read_messages=True, send_messages=False),
        mod_rolu: discord.PermissionOverwrite(send_messages=True)
    }
    bilgi_kat = await ctx.guild.create_category("📌 ｜ BİLGİLENDİRME")
    await bilgi_kat.create_text_channel("📜・kurallar", overwrites=izin_duyuru)
    await bilgi_kat.create_text_channel("📢・duyurular", overwrites=izin_duyuru)
    await bilgi_kat.create_text_channel("👋・hoş-geldin", overwrites=izin_duyuru)

    # 💬 SOHBET (Genel kanallar herkese açık, özel kanallar kilitli)
    sohbet_kat = await ctx.guild.create_category("💬 ｜ SOHBET & KÜLTÜR")
    await sohbet_kat.create_text_channel("💬・genel-sohbet")
    await sohbet_kat.create_text_channel("📷・medya-galerisi")
    await sohbet_kat.create_text_channel("🤖・bot-komut")
    # Sadece ilgili rollerin göreceği gizli kanallar:
    await sohbet_kat.create_text_channel("📚・felsefe-ve-edebiyat", overwrites=sadece_bu_rol_gorsun(kitap_rolu))
    await sohbet_kat.create_text_channel("🗣️・english-practice", overwrites=sadece_bu_rol_gorsun(ingilizce_rolu))

    # 🎮 OYUN (Tüm kanallar sadece ilgili oyunculara özel)
    oyun_kat = await ctx.guild.create_category("🎮 ｜ OYUN & EĞLENCE")
    await oyun_kat.create_text_channel("🤠・rdr2-kasabası", overwrites=sadece_bu_rol_gorsun(rdr2_rolu))
    await oyun_kat.create_text_channel("⚽・ea-fc-turnuva", overwrites=sadece_bu_rol_gorsun(fc_rolu))
    await oyun_kat.create_text_channel("⚔️・lol-mlbb-vadi", overwrites=sadece_bu_rol_gorsun(lol_rolu))
    await oyun_kat.create_text_channel("🧠・wordle-ve-trivia", overwrites=sadece_bu_rol_gorsun(trivia_rolu))

    # 💻 GELİŞTİRİCİ (Sadece Yazılımcılara özel)
    gelistirici_kat = await ctx.guild.create_category("💻 ｜ GELİŞTİRİCİ KÖŞESİ")
    await gelistirici_kat.create_text_channel("🛠️・bot-test-odası", overwrites=sadece_bu_rol_gorsun(yazilim_rolu))
    await gelistirici_kat.create_text_channel("🐍・python-sohbet", overwrites=sadece_bu_rol_gorsun(yazilim_rolu))

    # 🔊 SES KANALLARI
    ses_kat = await ctx.guild.create_category("🔊 ｜ SES KANALLARI")
    await ses_kat.create_voice_channel("🔊 Lobi Sohbet")
    await ses_kat.create_voice_channel("🎮 Yayın Odası")
    await ses_kat.create_voice_channel("🏆 Dereceli Maç Odası", user_limit=5)
    
    # Sadece B1+ İngilizce rolüne sahip olanların girebileceği ses odası
    izin_ses_ingilizce = {
        everyone: discord.PermissionOverwrite(view_channel=False),
        ingilizce_rolu: discord.PermissionOverwrite(view_channel=True, connect=True)
    }
    await ses_kat.create_voice_channel("🎧 İngilizce Konuşma Odası", overwrites=izin_ses_ingilizce)

    await ctx.send("✅ Efsanevi sunucu altyapısı, yetki sınırları ve özel kanallarla birlikte başarıyla inşa edildi!")

# YENİ GELENLERE OTOMATİK ROL, KANAL MESAJI VE ÖZEL DM SİSTEMİ
@bot.event
async def on_member_join(member):
    # 1. OTOMATİK ROL VERME KISMI
    rol = discord.utils.get(member.guild.roles, name="👤 Üye")
    if rol:
        try:
            await member.add_roles(rol)
        except discord.errors.Forbidden:
            print(f"Uyarı: {member.name} için rol verme yetkim yok!")

    # 2. KANALA ŞIK BİR HOŞ GELDİN KARTI ATMA KISMI
    # Sunucukur komutuyla açtığımız kanalın tam adını yazıyoruz (Emoji dahil birebir aynı olmalı)
    hosgeldin_kanali = discord.utils.get(member.guild.text_channels, name="👋・hoş-geldin")
    
    if hosgeldin_kanali:
        embed = discord.Embed(
            title="🌟 Sunucuya Yeni Biri Katıldı!",
            description=f"Aramıza hoş geldin {member.mention}! Seninle beraber kocaman bir aile olduk ve tam **{member.guild.member_count}** kişiye ulaştık.\n\nSohbete katılmadan önce `📌 ｜ BİLGİLENDİRME` kategorisine gidip menüden rollerini seçmeyi unutma!",
            color=discord.Color.brand_green()
        )
        
        # Eğer kullanıcının kendi profil fotoğrafı varsa onu, yoksa Discord'un varsayılan fotoğrafını koy
        if member.avatar:
            embed.set_thumbnail(url=member.avatar.url)
        else:
            embed.set_thumbnail(url=member.default_avatar.url)
            
        # Hangi sunucuya katıldığını alt bilgi olarak ekleyelim
        embed.set_footer(text=f"{member.guild.name} Yönetimi", icon_url=member.guild.icon.url if member.guild.icon else None)
            
        await hosgeldin_kanali.send(embed=embed)

    # 3. KULLANICIYA ÖZEL DM (DİREKT MESAJ) GÖNDERME KISMI
    try:
        dm_embed = discord.Embed(
            title=f"Hoş Geldin {member.name}! 🎉",
            description=f"**{member.guild.name}** sunucusuna katıldığın için çok mutluyuz.\n\nİçeride oyunlardan felsefeye, yazılımdan İngilizce pratiğe kadar seni bekleyen harika odalar var. Hadi hemen kanallara göz at ve maceraya başla!",
            color=discord.Color.blue()
        )
        await member.send(embed=dm_embed)
    except discord.errors.Forbidden:
        # Bazı kullanıcılar DM kutusunu yabancılara kapatır. Bot hata verip çökmesin diye bunu engelliyoruz.
        print(f"Uyarı: {member.name} adlı kullanıcının DM kutusu kapalı olduğu için mesaj iletilemedi.")
    # =========================================================
# YENİ NESİL AÇILIR MENÜ (DROPDOWN) ROL SEÇİM PANELİ
# =========================================================

class RolMenu(discord.ui.Select):
    def __init__(self):
        # Üyelerin menüde göreceği seçenekler ve açıklamaları
        secenekler = [
            discord.SelectOption(label="Geliştirici & Yazılımcı", value="💻 Geliştirici & Yazılımcı", emoji="💻", description="Yazılım sohbet kanallarını açar."),
            discord.SelectOption(label="Filozof & Kitap Kurdu", value="📚 Filozof & Kitap Kurdu", emoji="📚", description="Felsefe ve edebiyat kanalını açar."),
            discord.SelectOption(label="English B1+ Club", value="🗣️ English B1+ Club", emoji="🗣️", description="İngilizce pratik odalarını açar."),
            discord.SelectOption(label="Trivia & Kelime Ustası", value="🧠 Trivia & Kelime Ustası", emoji="🧠", description="Kelime oyunları kanalını açar."),
            discord.SelectOption(label="Fitness & Aktif Yaşam", value="🏃‍♂️ Fitness & Aktif Yaşam", emoji="🏃‍♂️", description="Spor muhabbetleri için."),
            discord.SelectOption(label="Vahşi Batı Efsanesi", value="🤠 Vahşi Batı Efsanesi", emoji="🤠", description="RDR2 kanalını açar."),
            discord.SelectOption(label="Yeşil Saha Ustası", value="⚽ Yeşil Saha Ustası", emoji="⚽", description="EA FC 26 turnuva kanalını açar."),
            discord.SelectOption(label="Vadi Savaşçısı", value="⚔️ Vadi Savaşçısı", emoji="⚔️", description="LoL ve MLBB kanallarını açar.")
        ]
        
        # max_values sayesinde kullanıcı aynı anda 8 tane bile seçebilir
        super().__init__(placeholder="İlgi alanlarını seç (Çoklu seçim yapabilirsin)...", min_values=0, max_values=len(secenekler), options=secenekler)

  # Kullanıcı menüden seçim yapıp tıkladığında çalışacak komut
    async def callback(self, interaction: discord.Interaction):
        # 1. ADIM: DİSCORD'U BEKLET
        await interaction.response.defer(ephemeral=True)

        uye = interaction.user
        secilen_degerler = self.values 
        
        tum_secilebilir_isimler = [opt.value for opt in self.options]
        
        # 2. ADIM: ROLLERİ SAKİNCE DAĞIT VE HATALARI YAKALA
        try:
            for isim in tum_secilebilir_isimler:
                rol = discord.utils.get(interaction.guild.roles, name=isim)
                if rol:
                    # Seçmiş ve rol yoksa ver
                    if isim in secilen_degerler and rol not in uye.roles:
                        await uye.add_roles(rol)
                    # Seçimden çıkarmış ve rol varsa geri al
                    elif isim not in secilen_degerler and rol in uye.roles:
                        await uye.remove_roles(rol)

            # Başarılı olursa bu mesajı at
            await interaction.followup.send("✅ Harika! Rollerin ve kanal erişimlerin başarıyla güncellendi.", ephemeral=True)
            
        # EĞER BOTUN YETKİSİ YETMİYORSA BU UYARIYI VER
        except discord.errors.Forbidden:
            await interaction.followup.send("⚠️ HATA: Sana bu rolü veremiyorum! Çünkü Discord sunucu ayarlarında benim kendi bot rolüm (PePe), vermek istediğim bu rollerden daha aşağıda kalıyor.", ephemeral=True)
        # BAŞKA BİR BİLİNMEYEN HATA VARSA BİLDİR
        except Exception as e:
            print(f"Hata detayı: {e}")
            await interaction.followup.send("⚠️ Beklenmedik bir hata oluştu, lütfen VS Code terminalini kontrol et.", ephemeral=True)
            # Menüyü karta yerleştirmek için taşıyıcı sınıf
class RolView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None) # Menünün sonsuza kadar açık kalması için
        self.add_item(RolMenu())
# Paneli Sunucuya Gönderme Komutu
@bot.command()
@commands.has_permissions(administrator=True)
async def rolpaneli(ctx):
    embed = discord.Embed(
        title="🎯 İlgi Alanları ve Oyun Rolleri",
        description="Sunucumuzda sadece ilgilendiğin kanalları görmek için aşağıdaki açılır menüden rollerini seçebilirsin.\n\n`Not:` Birden fazla rol seçebilir veya daha önce aldığın bir rolün tikini kaldırarak o kanalı gizleyebilirsin.",
        color=discord.Color.brand_green()
    )
    if ctx.guild.icon:
        embed.set_thumbnail(url=ctx.guild.icon.url)
        
    # Menüyü kanala gönder
    await ctx.send(embed=embed, view=RolView())

# =========================================================
# 🟩 WORDLE SİSTEMİ - %100 TAM VE EKSİKSİZ SÜRÜM 🟩
# =========================================================

@bot.command()
async def wordle(ctx):
    kullanici_id = str(ctx.author.id)
    tz = pytz.timezone('Europe/Istanbul')
    bugun = datetime.now(tz).strftime("%Y-%m-%d")
    
    with open("wordle.json", "r", encoding="utf-8") as f:
        try: db = json.load(f)
        except: db = {}

    # 1. Yeni Gün Kontrolü ve Rapor Gönderme (Emoji Filtreli)
    if db.get("tarih") and db.get("tarih") != bugun:
        eski_kelime = db.get("gunun_kelimesi", "BİLİNMİYOR")
        kazananlar = []
        kaybedenler = []
        
        for p_id, veri in db.get("oyuncular", {}).items():
            uye_metni = f"<@{p_id}>"
            if veri.get("durum") == "kazandi":
                kazananlar.append(f"🟩 {uye_metni} ({6 - veri.get('kalan_hak', 0)}/6)")
            elif veri.get("durum") == "kaybetti":
                kaybedenler.append(f"🟥 {uye_metni} (X/6)")
                
        rapor_kanali = None
        for kanal in ctx.guild.text_channels:
            if "wordle-ve-trivia" in kanal.name.lower():
                rapor_kanali = kanal
                break
                
        if rapor_kanali:
            embed = discord.Embed(title="📅 Wordle Gün Sonu Raporu", description=f"Dünün Kelimesi: **{eski_kelime}**", color=0xf1c40f)
            embed.add_field(name="🏆 Kazananlar", value="\n".join(kazananlar) if kazananlar else "Kimse kazanamadı.", inline=True)
            embed.add_field(name="💀 Kaybedenler", value="\n".join(kaybedenler) if kaybedenler else "Kimse kaybetmedi.", inline=True)
            await rapor_kanali.send(embed=embed)
            
        db["tarih"] = bugun
        db["gunun_kelimesi"] = random.choice(KELIME_HAVUZU)
        db["oyuncular"] = {} 
        
    elif not db.get("tarih"):
        db["tarih"] = bugun
        db["gunun_kelimesi"] = random.choice(KELIME_HAVUZU)
        db["oyuncular"] = {} 

    # 2. Günlük Limit Kontrolü
    if kullanici_id in db.get("oyuncular", {}):
        durum = db["oyuncular"][kullanici_id].get("durum")
        if durum in ["kazandi", "kaybetti"]:
            return await ctx.send(f"⚠️ {ctx.author.mention}, bugünün kelimesini zaten oynadın! Yeni kelime için gece **00:00'ı** bekle.")
    else:
        if "oyuncular" not in db:
            db["oyuncular"] = {}
        db["oyuncular"][kullanici_id] = {"kalan_hak": 6, "durum": "oynuyor", "tablo": []}
        with open("wordle.json", "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4)

    # 3. Özel Kanal Oluşturma
    kanal_adi = f"wordle-{ctx.author.name.lower()}"
    if discord.utils.get(ctx.guild.text_channels, name=kanal_adi):
        return await ctx.send(f"⚠️ {ctx.author.mention}, zaten açık bir oyun odan var! Oraya git: {discord.utils.get(ctx.guild.text_channels, name=kanal_adi).mention}")

    overwrites = {
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        ctx.author: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        bot.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
    }
    
    oyun_kanali = await ctx.guild.create_text_channel(kanal_adi, overwrites=overwrites)
    await ctx.send(f"🎮 Oyun odan hazır: {oyun_kanali.mention}")
    await oyun_kanali.send(f"Hoş geldin {ctx.author.mention}! Herkes için **Günün Kelimesi** belirlendi.\nToplam **6 hakkın** var. Başarılar!")


# --- WORDLE OYUN MOTORU ---
@bot.listen('on_message')
async def wordle_motoru(message):
    if message.author == bot.user: return
    
    beklenen_kanal_adi = f"wordle-{message.author.name.lower()}"
    if message.channel.name != beklenen_kanal_adi:
        return 

    tahmin = message.content.replace('i', 'İ').replace('ı', 'I').upper()
    if len(tahmin) != 5:
        return await message.channel.send("⚠️ Lütfen **5 harfli** bir kelime yaz!")

    # 4. Anlamsız Kelime (Sözlük) Koruması
    if tahmin not in KELIME_HAVUZU:
        return await message.channel.send(f"⚠️ **{tahmin}** kelime listesinde bulunamadı! *(Hakkın eksilmedi)*")

    with open("wordle.json", "r", encoding="utf-8") as f:
        db = json.load(f)

    hedef_kelime = db.get("gunun_kelimesi", "KİTAP")
    kullanici_id = str(message.author.id)

    if kullanici_id not in db.get("oyuncular", {}):
        return

    kalan_hak = db["oyuncular"][kullanici_id]["kalan_hak"]
    tablo_gecmisi = db["oyuncular"][kullanici_id].get("tablo", [])

    # 5. Hassas Renk Algoritması
    hedef_harfler = list(hedef_kelime)
    kutu_listesi = ["⬛"] * 5
    
    for i in range(5):
        if tahmin[i] == hedef_kelime[i]:
            kutu_listesi[i] = "🟩"
            hedef_harfler[i] = None 
            
    for i in range(5):
        if kutu_listesi[i] == "⬛" and tahmin[i] in hedef_harfler:
            kutu_listesi[i] = "🟨"
            hedef_harfler[hedef_harfler.index(tahmin[i])] = None
            
    sonuc = "".join(kutu_listesi)
    kalan_hak -= 1 
    
    tablo_gecmisi.append(sonuc)
    db["oyuncular"][kullanici_id]["tablo"] = tablo_gecmisi

    # 6. NYT Tarzı Oyun Sonu Ekranları
    if tahmin == hedef_kelime:
        db["oyuncular"][kullanici_id]["durum"] = "kazandi"
        
        tablo_metni = "\n".join(tablo_gecmisi)
        embed = discord.Embed(title="🏆 Günün Wordle Sonucu - KAZANDIN!", description=f"**Tebrikler!** Günün kelimesini doğru bildin.\n\n{tablo_metni}", color=0x2ecc71)
        embed.set_footer(text=f"Tahmin Sayısı: {6 - kalan_hak}/6 • Kanal 15 sn içinde silinecek")
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
        await message.channel.send(embed=embed)
        
    elif kalan_hak <= 0:
        db["oyuncular"][kullanici_id]["durum"] = "kaybetti"
        
        tablo_metni = "\n".join(tablo_gecmisi)
        embed = discord.Embed(title="💀 Hakkın Bitti - KAYBETTİN!", description=f"Günün Kelimesi: **{hedef_kelime}**\n\n{tablo_metni}", color=0xe74c3c)
        embed.set_footer(text="Tahmin Sayısı: X/6 • Kanal 15 sn içinde silinecek")
        embed.set_thumbnail(url=message.author.avatar.url if message.author.avatar else None)
        await message.channel.send(embed=embed)
        
    else:
        db["oyuncular"][kullanici_id]["durum"] = "oynuyor"
        await message.channel.send(f"`{tahmin}` | {sonuc}")

    db["oyuncular"][kullanici_id]["kalan_hak"] = kalan_hak
    with open("wordle.json", "w", encoding="utf-8") as f:
        json.dump(db, f, indent=4)

    if tahmin == hedef_kelime or kalan_hak <= 0:
        await asyncio.sleep(15)
        try: await message.channel.delete()
        except: pass

@bot.command(name="yardim", aliases=["help", "yardım", "komutlar", "menu"])
async def yardim_menusu(ctx):
    # Ana Çerçeve (Embed)
    embed = discord.Embed(
        title="🤖 Sunucu Asistanı - Kapsamlı Yardım Menüsü",
        description="Sunucumuzda kullanabileceğin tüm sistemler ve komutlar aşağıda listelenmiştir.\nKomutları kullanırken başlarına `!` koymayı unutma!",
        color=0x2b2d31 # Şık koyu tema rengi
    )

    # 🎮 Oyunlar & Eğlence Kategorisi
    embed.add_field(
        name="🎮 Eğlence & Oyunlar",
        value=(
            "**`!wordle`** : Özel odanda günlük kelime tahmin oyununu oynarsın.\n"
            "**`!oyunseç`** : Kararsız kaldığında bot sana rastgele bir oyun seçer.\n"
            "**`!sihirli_kure <soru>`** : Geleceği görmek için sihirli küreye bir soru sorarsın.\n"
            "**`!zar`** : Rastgele bir zar atar.\n"
            "**`!sarıl <@üye>`** : Etiketlediğin kişiye sevgiyle sarılırsın."
        ),
        inline=False
    )

    # 📊 Kullanıcı & Profil Kategorisi
    embed.add_field(
        name="📊 Kullanıcı Bilgileri",
        value=(
            "**`!profil`** : Kendi profil detaylarını görüntülersin.\n"
            "**`!avatar [@üye]`** : Kendi avatarını veya etiketlediğin kişinin avatarını büyütür.\n"
            "**`!istatistik [@üye]`** : Senin veya sunucunun güncel istatistiklerini gösterir."
        ),
        inline=False
    )

    # 🛠️ Genel Komutlar
    embed.add_field(
        name="🛠️ Genel Komutlar",
        value=(
            "**`!yardım`** : Şu an okuduğun bu kapsamlı rehberi açar.\n"
            "**`!selam`** : Bota selam verirsin, o da sana karşılık verir.\n"
            "**`!ping`** : Botun anlık gecikme süresini (ms) ölçer."
        ),
        inline=False
    )

    # 🛡️ Moderasyon ve Yönetim Kategorisi
    embed.add_field(
        name="🛡️ Moderasyon & Yönetim",
        value=(
            "**`!sil <miktar>`** : Kanaldan belirttiğin sayıda mesajı temizler.\n"
            "**`!oylama <konu>`** : Sunucuda evet/hayır şeklinde bir oylama başlatır.\n"
            "**`!rolpaneli`** : *(Yetkili)* Üyelerin tıklayarak rol alabileceği paneli kurar.\n"
            "**`!sunucukur`** : *(Yetkili)* Sunucu kanallarını ve altyapısını otomatik kurar."
        ),
        inline=False
    )

    # Alt Bilgi (Footer) - Emeğimizi yansıtan kısım
    embed.set_footer(
        text=f"Sorgulayan: {ctx.author.name} • 3 Günlük Kesintisiz Emeğin Eseri", 
        icon_url=ctx.author.avatar.url if ctx.author.avatar else None
    )
    
    # Sağ üste botun kendi profil fotoğrafını küçük resim (thumbnail) olarak ekliyoruz
    embed.set_thumbnail(url=bot.user.avatar.url if bot.user.avatar else None)
    
    # Menüyü Kanala Gönder
    await ctx.send(embed=embed)
# Token'ını buraya tırnakların arasına yapıştır:
# Token artık kodun içinde değil, gizli .env dosyasından çekiliyor!
keep_alive()
bot.run(os.getenv("TOKEN"))
