
class Zone:
    """
        Класс того как выглядит файл зоны, много конечно хранить но есть пару хитрых идей.

        Будте предельно аккуратны, сначала определите зону а потом уже дергайте ответы

        Возможно стоит переташить парсер сюды
    """
    name_zone = ""  # Возможно рудимент
    ttl = 0
    records_a = []
    records_aaaa = []
    records_ns = []
    records_mx = []
    records_cname = []
    dns_servers_zone = []

    def __str__(self):
        rec = f"Name zone: {self.name_zone}, TTL: {self.ttl}\n"
        rec_s = f"SOA: {self.dns_servers_zone}\n" \
                f"A: {self.records_a}\n" \
                f"AAAA: {self.records_aaaa}\n" \
                f"NS: {self.records_ns}\n" \
                f"MX: {self.records_mx}\n" \
                f"CNAME: {self.records_cname}\n"
        return rec + rec_s
