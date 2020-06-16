import copy

class Zone:
    """
        Класс того как выглядит файл зоны, много конечно хранить но есть пару хитрых идей.

        Будте предельно аккуратны, сначала определите зону а потом уже дергайте ответы

        Возможно стоит переташить парсер сюды

        Коды ощибок:
        ~~~~~~~~~~~~~~~~~~
            **-1** - В текушем файле зоны совпадения не обнаружены

    """
    name_zone = ""  # Возможно рудимент
    ttl = 0
    records_a = []
    records_aaaa = []
    records_ns = []
    records_mx = []
    records_cname = []
    dns_servers_zone = []

    # Поиск записи в листе этих записей, в сею секунду нет идей для зашиты от себя любимого,
    # поэтому запись SOA в NS искать не стоит
    def serch(self, record: list, records: list):
        for i in records:
            if record in i:
                return i

    # При запросе SOA возврашает и его ns, ns_ip
    def serch_soa_addition(self, serching: str):
        record = None
        for i in self.dns_servers_zone:
            if serching in i:
                record = copy.deepcopy(i)
                ns = record[3]
                ns, ip_ns = self.serch_ns_mx_addition(ns, self.records_ns)
                return record, ns, ip_ns

    # При запросе NS или MX так же возврашает и его ip
    def serch_ns_mx_addition(self, serching: str, records: list):
        record = None
        for i in records:
            if serching in i:
                record = copy.deepcopy(i)
                break

        if record is not None:
            ip = self.serch_ip(record[1])
            return record, ip

        return "-1"

    # Ишет ip во всех типах ip зон(A, AAAA)
    def serch_ip(self, host: str) -> list:
        for i in self.records_a:
            if host in i:
                return copy.deepcopy(i)
        for i in self.records_aaaa:
            if host in i:
                return copy.deepcopy(i)

    def __str__(self):
        rec = f"Name zone: {self.name_zone}, TTL: {self.ttl}\n"
        rec_s = f"SOA: {self.dns_servers_zone}\n" \
                f"A: {self.records_a}\n" \
                f"AAAA: {self.records_aaaa}\n" \
                f"NS: {self.records_ns}\n" \
                f"MX: {self.records_mx}\n" \
                f"CNAME: {self.records_cname}\n"
        return rec + rec_s
