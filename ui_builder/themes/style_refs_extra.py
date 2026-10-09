"""30 palet dan sistem bentuk tambahan untuk referensi gaya desain."""
from ui_builder.core.design import theme_of


def _ref(desc, primary, bg, text, font, width, radius, border_width, border_color, shadow, surface, ink="inherit",
         glass=False, glass_blur=18):
    return {
        "desc": desc,
        "theme": theme_of(primary, bg, text, font, width, glass=glass, glass_blur=glass_blur),
        "shape": {
            "radius": radius,
            "border_width": border_width,
            "border_color": border_color,
            "shadow": shadow,
        },
        "surface": surface,
        "ink": ink,
    }


EXTRA_DESIGN_REFS = {
    "Samudra terang": _ref(
        "Biru laut yang lapang, permukaan putih bersih, dan aksen aqua untuk produk perjalanan.",
        "#0284c7", "#f0f9ff", "#0c2d48", "Sans-serif modern", 820, 16, 1, "#bae6fd",
        "0 8px 24px rgba(2,132,199,.12)", "#ffffff"),
    "Hutan pinus": _ref(
        "Hijau hutan dan permukaan hangat untuk produk alam, kebun, dan komunitas.",
        "#166534", "#f4f8f1", "#183b2a", "Humanis", 780, 14, 1, "#cbd9c8",
        "0 4px 14px rgba(22,101,52,.12)", "#ffffff"),
    "Terakota hangat": _ref(
        "Warna tanah, kertas krem, dan garis halus untuk merek kerajinan dan kuliner.",
        "#c65d3a", "#fbf4ed", "#3d2923", "Serif elegan", 760, 10, 1, "#e7cfc0",
        "0 5px 16px rgba(94,55,38,.12)", "#fffdf9"),
    "Lavender lembut": _ref(
        "Lavender pastel dengan teks ungu tua dan permukaan yang menenangkan.",
        "#8b6bd6", "#f7f4ff", "#30254e", "Humanis", 740, 20, 1, "#e6dcff",
        "0 8px 22px rgba(112,82,179,.14)", "#ffffff"),
    "Koral cerah": _ref(
        "Koral dan merah muda untuk antarmuka ramah, ekspresif, dan berenergi.",
        "#f05d5e", "#fff6f4", "#402b2b", "Sans-serif modern", 760, 18, 1, "#ffd8d2",
        "0 7px 20px rgba(240,93,94,.16)", "#ffffff"),
    "Malam indigo": _ref(
        "Mode gelap berlapis dengan biru indigo, kontras jelas, dan aksen sian.",
        "#38bdf8", "#101426", "#e8edff", "Sans-serif modern", 800, 14, 1, "#293451",
        "0 8px 22px rgba(0,0,0,.32)", "#1a2038", "#e8edff"),
    "Matcha segar": _ref(
        "Hijau matcha, krem pucat, dan sudut membulat untuk produk keseharian.",
        "#668c43", "#f8f8ee", "#283322", "Humanis", 780, 18, 1, "#d9dfc9",
        "0 5px 16px rgba(65,95,43,.12)", "#fffef8"),
    "Pasir pantai": _ref(
        "Krem pasir, biru langit, dan garis lembut bernuansa liburan.",
        "#0e7490", "#fffaf0", "#3f3427", "Serif klasik", 780, 16, 1, "#eadfc9",
        "0 5px 18px rgba(14,116,144,.10)", "#ffffff"),
    "Biru teknologi": _ref(
        "Biru produk digital dengan kontras tinggi dan geometri yang rapi.",
        "#2563eb", "#f8fafc", "#111827", "Sans-serif modern", 860, 8, 1, "#cbd5e1",
        "0 6px 18px rgba(37,99,235,.14)", "#ffffff"),
    "Peach editorial": _ref(
        "Warna persik lembut, tipografi elegan, dan aksen merah bata untuk editorial.",
        "#c2413b", "#fff8f2", "#362a27", "Serif klasik", 720, 4, 1, "#ead9d0",
        "none", "#ffffff"),
    "Karamel klasik": _ref(
        "Palet karamel dan cokelat untuk restoran, kopi, serta toko artisan.",
        "#a16207", "#fffbeb", "#422006", "Serif elegan", 760, 12, 1, "#e7d6b3",
        "0 6px 18px rgba(120,75,20,.14)", "#ffffff"),
    "Mint klinis": _ref(
        "Hijau mint dan putih terang dengan garis rapi untuk layanan kesehatan.",
        "#0f9f83", "#f2fbf8", "#12352e", "Sans-serif modern", 820, 12, 1, "#c8e9df",
        "0 5px 16px rgba(15,159,131,.10)", "#ffffff"),
    "Merah editorial": _ref(
        "Aksen merah tegas pada kertas putih untuk berita dan publikasi modern.",
        "#c1121f", "#ffffff", "#202124", "Serif klasik", 760, 2, 1, "#dedede",
        "none", "#ffffff"),
    "Ungu premium": _ref(
        "Ungu gelap dan emas lembut memberi nuansa eksklusif tanpa kehilangan keterbacaan.",
        "#8b5cf6", "#171324", "#f4efff", "Serif elegan", 780, 16, 1, "#3f3557",
        "0 10px 28px rgba(8,5,18,.4)", "#241d35", "#f4efff"),
    "Teal butik": _ref(
        "Teal dalam, gading, dan bayangan tipis untuk katalog butik yang tenang.",
        "#0f766e", "#faf9f6", "#1f2933", "Humanis", 800, 14, 1, "#d9e3df",
        "0 7px 20px rgba(15,118,110,.12)", "#ffffff"),
    "Awan putih": _ref(
        "Latar putih dan abu lembut untuk antarmuka produk yang ringan dan universal.",
        "#475569", "#f8fafc", "#0f172a", "Sans-serif modern", 840, 12, 1, "#e2e8f0",
        "0 4px 14px rgba(15,23,42,.06)", "#ffffff"),
    "Kontras aksesibel": _ref(
        "Warna primer dan teks gelap dengan batas tegas untuk kontras yang mudah dibaca.",
        "#005fcc", "#ffffff", "#111111", "Sans-serif modern", 820, 6, 2, "#334155",
        "none", "#ffffff"),
    "Tinta dan tembaga": _ref(
        "Latar arang, aksen tembaga, dan karakter serif untuk pengalaman premium.",
        "#d18b55", "#191817", "#f2ece5", "Serif elegan", 760, 3, 1, "#49413a",
        "0 8px 22px rgba(0,0,0,.32)", "#262321", "#f2ece5"),
    "Pelangi pastel": _ref(
        "Palet pastel yang ceria, bentuk bulat, dan bayangan ringan untuk komunitas kreatif.",
        "#8b5cf6", "#fff8fc", "#352a46", "Humanis", 800, 24, 2, "#f0dff4",
        "0 8px 22px rgba(181,111,191,.14)", "#ffffff"),
    "Oranye energik": _ref(
        "Oranye kontras, latar putih, dan sudut ringkas untuk produk olahraga dan aksi.",
        "#ea580c", "#fffaf5", "#291c15", "Sans-serif modern", 820, 10, 1, "#fed7aa",
        "0 7px 18px rgba(234,88,12,.17)", "#ffffff"),
    "Hijau sage": _ref(
        "Sage dan krem lembut menghadirkan kesan tenang, natural, dan bersahaja.",
        "#647b63", "#f7f7f1", "#283329", "Serif elegan", 760, 14, 1, "#dce0d5",
        "0 5px 16px rgba(70,95,72,.10)", "#ffffff"),
    "Biru es": _ref(
        "Biru es, latar dingin, dan kontras bersih untuk dashboard dan analitik.",
        "#0369a1", "#f0f9ff", "#0c2438", "Sans-serif modern", 860, 8, 1, "#cfe8f5",
        "0 5px 16px rgba(3,105,161,.11)", "#ffffff"),
    "Burgundy mewah": _ref(
        "Burgundy dan champagne untuk kesan hangat, berkelas, dan berani.",
        "#8f2635", "#faf4ef", "#331c21", "Serif klasik", 760, 10, 1, "#e8d4ca",
        "0 8px 20px rgba(87,25,37,.14)", "#ffffff"),
    "Graphite pro": _ref(
        "Grafit, putih, dan satu aksen cyan untuk perangkat kerja yang fokus.",
        "#0891b2", "#f3f4f6", "#171923", "Sans-serif modern", 880, 8, 1, "#d1d5db",
        "0 6px 18px rgba(17,24,39,.10)", "#ffffff"),
    "Retro arcade": _ref(
        "Latar biru malam dengan magenta terang, garis piksel, dan ritme permainan retro.",
        "#f472b6", "#111827", "#f9a8d4", "Monospace", 820, 2, 2, "#7c3aed",
        "0 0 18px rgba(244,114,182,.28)", "#1f2937", "#f9a8d4"),
    "Matahari senja": _ref(
        "Gradien warna senja diterjemahkan ke aksen jingga di atas latar aprikot.",
        "#e85d3f", "#fff7ed", "#3b241f", "Humanis", 800, 18, 1, "#fed7aa",
        "0 8px 22px rgba(232,93,63,.16)", "#ffffff"),
    "Lilac digital": _ref(
        "Lilac, biru elektrik, dan permukaan terang untuk produk kreatif digital.",
        "#7c3aed", "#f7f5ff", "#231942", "Sans-serif modern", 820, 18, 1, "#ded6ff",
        "0 8px 22px rgba(124,58,237,.14)", "#ffffff"),
    "Batu alam": _ref(
        "Abu batu, putih hangat, dan garis natural untuk interior serta arsitektur.",
        "#57534e", "#fafaf9", "#292524", "Serif elegan", 780, 4, 1, "#d6d3d1",
        "0 4px 14px rgba(41,37,36,.08)", "#ffffff"),
    "Lime elektrik": _ref(
        "Aksen lime yang berani di atas tinta gelap untuk eksperimen digital futuristik.",
        "#a3e635", "#10130b", "#eff8d9", "Monospace", 820, 6, 1, "#3f4d20",
        "0 0 20px rgba(163,230,53,.18)", "#1b2112", "#eff8d9"),
    "Kaca samudra": _ref(
        "Aqua, biru malam, dan panel transparan untuk permukaan kaca yang segar.",
        "#22d3ee", "#0e1b2d", "#e6fbff", "Humanis", 840, 22, 1, "rgba(255,255,255,.35)",
        "0 10px 28px rgba(34,211,238,.20)", "rgba(23,45,64,.55)", "#e6fbff", glass=True, glass_blur=22),
}
