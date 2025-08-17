import discord
from discord.ext import commands
import requests
import os
import random

kullanici_puanlari ={}
kullanici_su = {}
kullanici_elektrik = {}


# Botun Discord API'ye bağlanması için gerekli izinler
intents = discord.Intents.default()
intents.message_content = True  # Botun mesaj içeriğine erişimine izin veriyoruz.

# Botu başlatıyoruz
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} olarak giriş yaptık!')  # Botun başarılı bir şekilde bağlandığını belirten mesaj

veri_listesi = [
    "Değişen iklim koşulları, birçok hayvan ve bitki türünün yaşam alanlarını tehdit ederek yok olmalarına neden oluyor.",
    "İklim değişikliği, kuraklık, sel, kasırga ve orman yangınları gibi aşırı hava olaylarının sıklığını ve şiddetini artırıyor.",
    "Kutuplardaki buzullar eriyor ve okyanuslar ısınıyor, bu da deniz seviyesinin yükselmesine ve kıyı bölgelerinin tehlikeye girmesine neden oluyor."
]

@bot.command()
async def bilgi_gonder(ctx):
    bilgi=random.choice(veri_listesi)
    await ctx.send(bilgi)



# Çevre Dostu Sorular & Cevaplar (Quiz)
@bot.command()
async def cevre_sorusu(ctx):
    sorular = [
        ("Plastiklerin doğada ne kadar sürede çözüldüğünü biliyor musun?", ["Yüzyıllar", "Günler", "Saatler"], "Yüzyıllar"),
        ("Geri dönüşüm kutusuna hangi malzeme atılabilir?", ["Plastik", "Yemek Artığı", "Ayakkabı"], "Plastik"),
        ("Kompost yapmak için hangi malzeme kullanılır?", ["Kahve Telvesi", "Plastik", "Cam Şişe"], "Kahve Telvesi")
    ]
    soru, cevaplar, dogru_cevap = random.choice(sorular)
    random.shuffle(cevaplar)
    
    await ctx.send(f"Soru: {soru}\nCevap seçenekleri: {', '.join(cevaplar)}")
    
    def check(message):
        return message.author == ctx.author and message.content.lower() in [cevap.lower() for cevap in cevaplar]

    try:
        cevap = await bot.wait_for("message", check=check, timeout=30)
        if cevap.content.lower() == dogru_cevap.lower():
            await ctx.send("Tebrikler, doğru cevap!")
        else:
            await ctx.send(f"Yanlış cevap. Doğru cevap: {dogru_cevap}")
    except TimeoutError:
        await ctx.send("Zaman doldu! Cevap veremediniz.")


# Çevre dostu görevler
@bot.command()
async def cevre_gorevi(ctx):
    gorevler = [
        "Bugün 10 dakika boyunca dışarıda çöpleri topla! ♻️",
        "Evde plastik yerine kağıt kullanmaya çalış! 📜",
        "Kompost yapmak için eski yemekleri sakla! 🥕"
        "Bir gün boyunda plastik pet şişe kullanmak yerine cam şişe kullan!!!"
        "Bugünlük kıyafetlerini düşük sıcaklıkta yıka! "
        "Birgün boyunca kıyafetlerini kurutma makinesi yerine ipte kurut!!"
        "Bugün dışarı çıkarken bir toplu taşıma aracının kullanımı veya bisikletle git mesafesi. Arabanın bir günlüğüne kullan."
        "Bugün market alışverişine giderken bez çanta kullan ve plastik poşetlerden uzak dur."
        "Bugün işe giderken kendi termosunu alarak tek kullanımlık kahve bardaklarının önüne geç!"
        "Bugün eski kıyafetlerini ihtiyacı olan birine vererek döngüsel ekonomiye katkı sağla:)"
        "Bugün evdeki tüm kullanılmayan elektronik aletleri fişten çekerek 'vampir' enerjisini durdur...🦇"
        "Evden çıkmadan önce su ve gaz vanalarını kontrol et."
        "Yeni bir ürün almadan önce gerçekten ihtiyacın olup olmadığını sorgula???"
    ]
    gorev = random.choice(gorevler)
    await ctx.send(f"Bugünün çevre görevi: {gorev}")

# Günlük bilgi aktarımı
@bot.command()
async def bilgi_aktarımı(ctx):
    bilgiler = [
        "Sanayi devriminden bu yana Dünya_nın sıcaklığı 1.1 C arttı. Bu artışın büyük bir kısmı son 30-40 yılda oldu."
        "Ormanlar, atmosferdeki karbondioksiti emerek önemli bir karbon yutağı oluşturur. Her yıl kesilen ormanlar, iklim değişikliği ile mucadelede en büyük engellerden biridir."
        "Son yüz yılda, küresel deniz seviyesi 15-20 cm yükseldi. Bu durumun en büyük nedeni buzulların erimesi ile ısıyan suyun genleşmesidir."
        "Karbondioksit, metan ve azot oksit gibi gazlar, Güneş'ten gelen ısının Dünya'nın atmosferinde tutulmasına neden olarak gezegenin ısınmasına yol açar."
        "İklim değişikliği, kasırgalar, seller, kuraklıklar ve orman yangınları gibi aşırı hava olaylarının sıklığını ve şiddetini artırıyor."
        "Atmosferdeki karbondioksitin okyanuslar tarafından emilmesi, suyun pH değerini düşürerek deniz canlılarının kabuk ve iskelet yapılarını bozuyor."
        "İklim değişikliği, canlı türlerinin yaşam alanlarını daraltarak ve ekosistemleri bozarak biyolojik çeşitliliği tehdit ediyor. Birçok hayvan ve bitki türü, değişen sıcaklıklara ve hava koşullarına uyum sağlayamıyor. Bu durum, bazı türlerin neslinin tükenmesine yol açarken, bazı türlerin de göç etmek zorunda kalmasına neden oluyor."
        "İklim değişikliği, kuraklık ve sel gibi aşırı hava olayları, tarımsal verimi düşürüyor ve gıda güvenliğini tehdit ediyor."
        "İklim değişikliği, sıcak hava dalgaları, solunum yolu hastalıkları ve bulaşıcı hastalıkların yayılmasına neden olabiliyor."
        "İklim değişikliği, deniz seviyesinin yükselmesi ve aşırı yağışlar, kıyı kentlerindeki binalara, yollara ve köprülere zarar veriyor."
        "İklim değişikliği ile mücedele için fosil yakıtlar yerine güneş, rüzgar ve jeotermal gibi temiz enerji kaynaklarına geçiş, sera gazı emisyonlarını azaltmanın en etkili yollarından biridir."
        "İklim değişikliği ile mücadele için evlerde ve sanayide kullanılan enerjiyi daha verimli hale getirmek, enerji tüketimini ve dolayısıyla emisyonları düşürmeye yardımcı olur."
        "İklim değişikliği ile mücadele için elektrikli araçlar ve toplu taşıma gibi çevre dostu ulaşım yöntemlerinin teşvik edilmesi, karbon salımını azaltır."
        "Türkiye'de ortalama sıcaklıklar küresel ortalamadan daha hızlı artıyor. Bu durum, özellikle yaz aylarında sıcak hava dalgalarının daha sık ve şiddetli yaşanmasına neden oluyor."
        "Yağış rejimindeki değişiklikler ve buharlaşma artışı, Türkiye'deki su kaynaklarını tehdit ediyor. Özellikle iç Anadolu ve Güneydoğu Anadolu bölgelerinde kuraklık riski artıyor."
        "Su stresi, sel ve kuraklıklar tarımsal verimi düşürüyor. Bazı geleneksel ürünlerin ekim alanları değişirken, Akdeniz ve Ege'de zeytin ve turunçgiller gibi ürünlerin üretimi risk altında."
    ]
    bilgi = random.choice(bilgiler)
    await ctx.send(f"Bu bilgiyi biliyor muydunuz???{bilgi}")
    
# Günlük görevleri
@bot.command()
async def gunluk_gorevler(ctx):
    görevler = [
        "Bugün plastik şişe yerine metal bir şişe kullan!!",
        "Evde geri dönüşüm kutusu oluştur ve tüm aileye bunu öğret!",
        "Dışarı çıkarken kendi alışveriş torbanı almayı unutma!"
    ]
    görev = random.choice(görevler)
    await ctx.send(f"Bugün bu görevi yapmayı unutma: {görev}")

    puan_ekle(ctx.author.id, 20)

@bot.command()
async def gorseller(ctx):
    try:
        # 'images' klasöründeki tüm dosyaların listesini alıyoruz.
        files = os.listdir('images')
        if not files:  # Eğer klasör boşsa kullanıcıya bilgi veriyoruz.
            await ctx.send("Resim klasörü boş!")
            return
        
        # Rastgele bir dosya seçiyoruz.
        img_name = random.choice(files)
        
        # Dosyayı açıp kullanıcıya gönderiyoruz.
        with open(f'images/{img_name}', 'rb') as f:
            picture = discord.File(f)
        await ctx.send(file=picture)
    except FileNotFoundError:
        await ctx.send("Resim klasörü bulunamadı! Lütfen 'images' klasörünün mevcut olduğundan emin olun.")
    except Exception as e:
        await ctx.send(f"Bir hata oluştu: {e}")

@bot.command()
async def su_ekle(ctx, miktar: int):
    """Kullanıcı su kullanım miktarını ekler."""
    kullanici_id = str(ctx.author.id)
    try:
        miktar = int(miktar)
        await ctx.send(f"Toplam {miktar} kadar su kullandınız.")
    except:
        await ctx.send("Lütfen geçerli bir sayı girin. Örneğin = !su_ekle 5 ")
        return
    puan_ekle(ctx, kullanici_id, puan)

async def puan_ekle(ctx, kullanici_id, puan):
    if kullanici_id not in kullanici_puanlari:
        kullanici_puanlari[kullanici_id] = 0
        kullanici_puanlari[kullanici_id] += puan 
        await ctx.send(f"{kullanici_id} size {puan} kadar puan ekledi. Şuan toplam puanınız ={kullanici_puanlari[kullanici_id]}")

@bot.command()
async def puan(ctx):
    kullanici_id = ctx.author.id
    if kullanici_id in kullanici_puanlari:
        puan = kullanici_puanlari[kullanici_id]
        await ctx.send(f"Heyy! Şuan puanın: {puan}")
    else:
        await ctx.send(f"Üzgünüm ama şuan hiç puanın yok:( Ama hemen görevlerini tamamlayarak ve soruları çözerek puan kazana bilirsin!!! İyi şanslarr.😊")

    



bot.run("token")
