"""Initial catalog data for the local academic demonstration.

MongoDB keeps these records after their first insert.
"""

STARTER_SERVICES = [
    {"name": "Diagnóstico completo", "category": "Diagnóstico", "description": "Investigamos lentidão, travamentos e falhas para encontrar a causa antes de qualquer reparo.", "price": 49.90, "duration": "Até 1 dia útil", "icon": "⌕", "featured": True, "active": True},
    {"name": "Limpeza preventiva", "category": "Manutenção", "description": "Limpeza interna, remoção de poeira e revisão térmica para seu computador respirar melhor.", "price": 119.90, "duration": "1 a 2 dias úteis", "icon": "✳", "featured": True, "active": True},
    {"name": "Formatação e instalação", "category": "Software", "description": "Sistema operacional reinstalado, drivers atualizados e computador pronto para usar.", "price": 159.90, "duration": "1 a 2 dias úteis", "icon": "↻", "featured": True, "active": True},
    {"name": "Upgrade de memória RAM", "category": "Upgrade", "description": "Instalação e configuração de memória para trabalhar com mais fluidez. Peça cobrada à parte.", "price": 89.90, "duration": "Até 1 dia útil", "icon": "▤", "featured": False, "active": True},
    {"name": "Instalação de SSD", "category": "Upgrade", "description": "Instalação de SSD e migração dos seus dados para um computador mais rápido. Peça à parte.", "price": 139.90, "duration": "1 a 2 dias úteis", "icon": "▣", "featured": False, "active": True},
    {"name": "Reparo de notebook", "category": "Reparo", "description": "Análise e reparo de notebooks com problemas de inicialização, tela, teclado ou energia.", "price": 179.90, "duration": "2 a 5 dias úteis", "icon": "⌘", "featured": False, "active": True},
    {"name": "Remoção de vírus", "category": "Software", "description": "Remoção de programas maliciosos, revisão de segurança e orientação para prevenção.", "price": 99.90, "duration": "Até 1 dia útil", "icon": "⛨", "featured": False, "active": True},
    {"name": "Montagem de PC", "category": "Montagem", "description": "Montagem cuidadosa, organização de cabos e configuração inicial. Escolha as peças que quer incluir no orçamento.", "price": 249.90, "duration": "1 a 3 dias úteis", "icon": "⚙", "featured": True, "active": True, "assembly": True},
    {"name": "Limpeza avançada de notebook", "category": "Manutenção", "description": "Desmontagem técnica, limpeza profunda e troca da pasta térmica do processador.", "price": 159.90, "duration": "1 a 2 dias úteis", "icon": "✧", "featured": False, "active": True},
    {"name": "Troca de pasta térmica", "category": "Manutenção", "description": "Substituição da pasta térmica para ajudar a controlar as temperaturas do processador.", "price": 69.90, "duration": "Até 1 dia útil", "icon": "◉", "featured": False, "active": True},
    {"name": "Reparo de placa-mãe", "category": "Reparo", "description": "Análise técnica de falhas de energia, inicialização e componentes da placa-mãe.", "price": 229.90, "duration": "3 a 7 dias úteis", "icon": "▦", "featured": False, "active": True},
    {"name": "Reparo de fonte de alimentação", "category": "Reparo", "description": "Diagnóstico da fonte, testes de estabilidade e avaliação de reparo ou substituição.", "price": 99.90, "duration": "2 a 4 dias úteis", "icon": "ϟ", "featured": False, "active": True},
    {"name": "Instalação de placa de vídeo", "category": "Upgrade", "description": "Instalação, conexão e configuração de placa de vídeo. A peça pode ser incluída no orçamento.", "price": 119.90, "duration": "Até 1 dia útil", "icon": "▰", "featured": False, "active": True},
    {"name": "Instalação de processador", "category": "Upgrade", "description": "Instalação de processador compatível e revisão do sistema de refrigeração.", "price": 119.90, "duration": "Até 1 dia útil", "icon": "▣", "featured": False, "active": True},
    {"name": "Instalação de placa-mãe", "category": "Upgrade", "description": "Troca da placa-mãe, montagem dos componentes e teste de inicialização.", "price": 229.90, "duration": "1 a 2 dias úteis", "icon": "▦", "featured": False, "active": True},
    {"name": "Backup e recuperação de arquivos", "category": "Dados", "description": "Cópia de segurança e tentativa de recuperação de documentos, fotos e arquivos pessoais.", "price": 139.90, "duration": "1 a 3 dias úteis", "icon": "↥", "featured": False, "active": True},
    {"name": "Configuração de rede Wi-Fi", "category": "Redes", "description": "Configuração de roteador, rede sem fio e conexão dos dispositivos da sua casa.", "price": 119.90, "duration": "Até 1 dia útil", "icon": "⌁", "featured": False, "active": True},
    {"name": "Instalação de impressora", "category": "Periféricos", "description": "Instalação de impressora, drivers e configuração para uso no computador ou rede.", "price": 69.90, "duration": "Até 1 dia útil", "icon": "▤", "featured": False, "active": True},
    {"name": "Configuração de computador novo", "category": "Software", "description": "Primeira configuração, atualizações, aplicativos essenciais e transferência inicial de arquivos.", "price": 129.90, "duration": "Até 1 dia útil", "icon": "✦", "featured": False, "active": True},
    {"name": "Otimização de desempenho", "category": "Software", "description": "Revisão de inicialização, atualizações e configurações para deixar o sistema mais ágil.", "price": 89.90, "duration": "Até 1 dia útil", "icon": "↗", "featured": False, "active": True},
    {"name": "Instalação de pacote Office", "category": "Software", "description": "Instalação e configuração de aplicativos de produtividade com licença fornecida pelo cliente.", "price": 59.90, "duration": "Até 1 dia útil", "icon": "▧", "featured": False, "active": True},
    {"name": "Instalação de sistema Linux", "category": "Software", "description": "Instalação de distribuição Linux, drivers e configuração inicial do ambiente.", "price": 129.90, "duration": "1 a 2 dias úteis", "icon": "⌘", "featured": False, "active": True},
    {"name": "Configuração de controle parental", "category": "Software", "description": "Configuração de contas e controles de segurança para uso familiar mais tranquilo.", "price": 69.90, "duration": "Até 1 dia útil", "icon": "⛨", "featured": False, "active": True},
    {"name": "Instalação de cooler e fans", "category": "Upgrade", "description": "Instalação de ventoinhas e revisão do fluxo de ar do gabinete. Peças à parte.", "price": 79.90, "duration": "Até 1 dia útil", "icon": "❋", "featured": False, "active": True},
    {"name": "Instalação de water cooler", "category": "Upgrade", "description": "Instalação e teste de sistema de refrigeração líquida compatível.", "price": 149.90, "duration": "Até 1 dia útil", "icon": "❄", "featured": False, "active": True},
    {"name": "Organização de cabos", "category": "Montagem", "description": "Organização interna dos cabos e melhoria do fluxo de ar do computador.", "price": 89.90, "duration": "Até 1 dia útil", "icon": "⌇", "featured": False, "active": True},
    {"name": "Montagem de setup gamer", "category": "Montagem", "description": "Montagem do computador e conexão inicial dos periféricos do seu setup.", "price": 299.90, "duration": "1 a 3 dias úteis", "icon": "▣", "featured": False, "active": True, "assembly": True},
    {"name": "Reparo de tela de notebook", "category": "Reparo", "description": "Diagnóstico e substituição de tela de notebook. A peça é cotada após confirmação do modelo.", "price": 189.90, "duration": "2 a 5 dias úteis", "icon": "▱", "featured": False, "active": True},
    {"name": "Troca de teclado de notebook", "category": "Reparo", "description": "Substituição de teclado com defeito após identificação do modelo compatível.", "price": 119.90, "duration": "2 a 5 dias úteis", "icon": "⌨", "featured": False, "active": True},
    {"name": "Reparo de conector de energia", "category": "Reparo", "description": "Avaliação e reparo do conector de alimentação de notebooks e computadores.", "price": 149.90, "duration": "2 a 5 dias úteis", "icon": "ϟ", "featured": False, "active": True},
    {"name": "Clonagem de HD para SSD", "category": "Dados", "description": "Migração do sistema e arquivos de um HD para SSD, com verificação da inicialização.", "price": 119.90, "duration": "1 a 2 dias úteis", "icon": "⇢", "featured": False, "active": True},
    {"name": "Recuperação de HD externo", "category": "Dados", "description": "Diagnóstico de unidade externa e tentativa de recuperar arquivos acessíveis.", "price": 129.90, "duration": "2 a 5 dias úteis", "icon": "▰", "featured": False, "active": True},
    {"name": "Instalação de webcam e periféricos", "category": "Periféricos", "description": "Instalação de webcam, headset, teclado, mouse e demais acessórios do computador.", "price": 59.90, "duration": "Até 1 dia útil", "icon": "◎", "featured": False, "active": True},
    {"name": "Suporte remoto", "category": "Suporte", "description": "Ajuda remota para resolver configurações e dúvidas simples de software.", "price": 49.90, "duration": "Até 2 horas", "icon": "⌁", "featured": False, "active": True},
    {"name": "Consultoria para upgrade", "category": "Consultoria", "description": "Recomendação de peças compatíveis para melhorar o computador dentro do seu orçamento.", "price": 39.90, "duration": "Até 1 dia útil", "icon": "✧", "featured": False, "active": True},
    {"name": "Montagem e configuração de servidor", "category": "Redes", "description": "Montagem básica e configuração inicial de servidor para pequeno escritório.", "price": 399.90, "duration": "2 a 4 dias úteis", "icon": "▥", "featured": False, "active": True},
]


def make_parts():
    catalog = {
        "Processador": [
            ("AMD Ryzen 5 5600GT", 899), ("AMD Ryzen 5 5600", 799), ("AMD Ryzen 5 5500", 649), ("AMD Ryzen 7 5700X", 1099),
            ("AMD Ryzen 7 5700G", 1199), ("AMD Ryzen 7 5800X", 1399), ("AMD Ryzen 9 5900X", 1999),
            ("AMD Ryzen 5 7600", 1399), ("AMD Ryzen 5 7600X", 1599), ("AMD Ryzen 7 7700", 1999), ("AMD Ryzen 7 7800X3D", 2699), ("AMD Ryzen 9 7900X", 3199),
            ("Intel Core i3-12100F", 599), ("Intel Core i3-14100F", 749), ("Intel Core i5-12400F", 899), ("Intel Core i5-13400F", 1199),
            ("Intel Core i5-14400F", 1399), ("Intel Core i5-14600K", 1899), ("Intel Core i7-12700KF", 1699), ("Intel Core i7-14700K", 2699),
            ("Intel Core i9-14900K", 3799)],
        "Placa-mãe": [
            ("Gigabyte A520M K V2 AM4", 399), ("ASUS Prime A520M-E AM4", 449), ("MSI B550M PRO-VDH AM4", 699), ("Gigabyte B550M DS3H AM4", 649),
            ("ASUS TUF Gaming B550M-PLUS AM4", 999), ("MSI B550 Tomahawk AM4", 1199), ("ASUS Prime B650M-A AM5", 1199),
            ("Gigabyte B650M Gaming WiFi AM5", 1099), ("MSI PRO B650M-A WiFi AM5", 1399), ("ASUS TUF Gaming B650-PLUS AM5", 1799),
            ("ASUS Prime H610M-E LGA1700", 599), ("Gigabyte H610M H LGA1700", 549), ("MSI PRO B760M-P LGA1700", 899),
            ("ASUS TUF Gaming B760M-PLUS LGA1700", 1499), ("Gigabyte Z790 UD LGA1700", 1899)],
        "Placa de vídeo": [
            ("MSI GeForce GTX 1650 4GB", 999), ("Gigabyte GeForce RTX 3050 6GB", 1399), ("ASUS Dual GeForce RTX 3060 12GB", 1899),
            ("MSI GeForce RTX 4060 Ventus 2X 8GB", 2199), ("Gigabyte GeForce RTX 4060 Ti 8GB", 2899), ("ASUS Dual GeForce RTX 4070 12GB", 3999),
            ("Gigabyte GeForce RTX 4070 SUPER 12GB", 4599), ("MSI GeForce RTX 4070 Ti SUPER 16GB", 6299), ("ASUS GeForce RTX 4080 SUPER 16GB", 8999),
            ("ASRock Radeon RX 6600 8GB", 1499), ("XFX Radeon RX 7600 8GB", 1899), ("PowerColor Radeon RX 7600 XT 16GB", 2299),
            ("ASRock Radeon RX 7700 XT 12GB", 3199), ("XFX Radeon RX 7800 XT 16GB", 3699), ("Sapphire Radeon RX 7900 GRE 16GB", 4499)],
        "Memória RAM": [
            ("Kingston Fury Beast 8GB DDR4 3200MHz", 139), ("Kingston Fury Beast 16GB DDR4 3200MHz", 249), ("Corsair Vengeance LPX 16GB DDR4 3200MHz", 269),
            ("Kingston Fury Beast 32GB (2x16) DDR4 3200MHz", 479), ("Corsair Vengeance 32GB (2x16) DDR4 3600MHz", 549),
            ("Kingston Fury Beast 16GB DDR5 5200MHz", 329), ("Corsair Vengeance 16GB DDR5 5600MHz", 369),
            ("Kingston Fury Beast 32GB (2x16) DDR5 5600MHz", 649), ("Corsair Vengeance 32GB (2x16) DDR5 6000MHz", 749),
            ("Kingston Fury Beast 64GB (2x32) DDR5 6000MHz", 1399)],
        "Armazenamento": [
            ("Kingston A400 SSD SATA 240GB", 149), ("Crucial BX500 SSD SATA 480GB", 249), ("Kingston NV2 NVMe 500GB", 299),
            ("WD Green SN350 NVMe 1TB", 449), ("Kingston NV2 NVMe 1TB", 499), ("WD Black SN770 NVMe 1TB", 699),
            ("Kingston KC3000 NVMe 2TB", 1199), ("Seagate BarraCuda HD 1TB", 329), ("Seagate BarraCuda HD 2TB", 449), ("WD Blue HD 4TB", 799)],
        "Fonte": [
            ("MSI MAG A550BN 550W 80 Plus Bronze", 329), ("Corsair CV550 550W 80 Plus Bronze", 379), ("Cooler Master MWE 650W 80 Plus Bronze", 449),
            ("XPG Pylon 650W 80 Plus Bronze", 429), ("Corsair CX650 650W 80 Plus Bronze", 499), ("XPG Core Reactor 750W 80 Plus Gold", 699),
            ("Corsair RM750e 750W 80 Plus Gold", 799), ("MSI MAG A850GL 850W 80 Plus Gold", 849), ("Corsair RM850x 850W 80 Plus Gold", 1099),
            ("XPG Core Reactor II 1000W 80 Plus Gold", 1299)],
        "Gabinete": [
            ("Mancer Goblin Mini Tower", 199), ("Cooler Master Q300L Mini Tower", 349), ("Montech X3 Mesh Mid Tower", 399),
            ("Corsair 4000D Airflow Mid Tower", 699), ("NZXT H5 Flow Mid Tower", 799), ("Lian Li Lancool 216 Mid Tower", 899),
            ("Thermaltake View 270 TG ARGB Mid Tower", 699), ("Redragon Wideload Lite Mid Tower", 349)],
        "Cooler e refrigeração": [
            ("DeepCool AG400 Air Cooler", 179), ("Cooler Master Hyper 212 Black Edition", 299), ("DeepCool AK620 Air Cooler", 499),
            ("Noctua NH-D15 Air Cooler", 799), ("Rise Mode Z3 120mm Fan", 29), ("Cooler Master SickleFlow 120mm ARGB Fan", 69),
            ("DeepCool LE500 240mm Water Cooler", 399), ("Corsair iCUE H100i 240mm Water Cooler", 899), ("NZXT Kraken 360mm Water Cooler", 1399)],
        "Monitor": [
            ("LG 24MP400 24 polegadas Full HD 75Hz", 599), ("AOC 24G2S 24 polegadas Full HD 165Hz", 899),
            ("Samsung Odyssey G3 24 polegadas Full HD 180Hz", 999), ("LG UltraGear 27 polegadas QHD 165Hz", 1699),
            ("AOC Hero 27 polegadas QHD 180Hz", 1799), ("Samsung Odyssey G5 32 polegadas QHD 165Hz", 2299)],
        "Periférico": [
            ("Logitech MK120 Teclado e Mouse USB", 99), ("Redragon Kumara Teclado Mecânico", 199), ("Logitech G203 Mouse Gamer", 149),
            ("HyperX Cloud Stinger 2 Headset", 299), ("Logitech C920 Webcam Full HD", 399), ("TP-Link Archer T3U Adaptador Wi-Fi USB", 129)],
    }
    return [{"name": name, "category": category, "price": price, "active": True}
            for category, products in catalog.items() for name, price in products]

STARTER_PARTS = make_parts()
