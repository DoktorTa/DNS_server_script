from Zone import Zone


class Zone_parse:
    """
        Класс отвечаюший за формирование обьекта зоны.
        Вполне возможно что скоро данный класс будет вырезан и его задачи лягут на класс зоны.

    Методы:
    ~~~~~~~~~~~~~~~~~~
        **generation_zone_object** - Генерирует зону по файлу. \n
        **ime_convert** - Конвертируете время из w, d, h, m в s,
            работает со строками имеюшими только один модификатор времени (w, W, d, D, h, H, m, M),
            будет "2w4d" и че там получиться будет определено саммым большим модификатором (w > d > h > m). \n

        Следуюшие методы помоему предстовляют лютую говно-кодину, надо это причесать.\n
        **record_soa** - SOA.\n
        **record_mx_recor** - MX.\n
        **record_a_aaaa** - A, AAAA.\n
        **record_ns_cname** - CNAME.\n

    """

    def __init__(self):
        pass

    # Генерирует обьект зоны на файле
    def generation_zone_object(self, path: str):
        z = Zone()
        addition = ""
        with open(path, "r") as file_z:
            for line in file_z:
                line = line.replace("(", " ")
                line = line.replace(")", " ")
                line_list = line.split()
                if "$ORIGIN" in line_list:
                    addition = line_list[1]
                elif "$TTL" in line_list:
                    z.ttl = self.time_convert(line_list[1])
                elif "A" in line_list:
                    z.records_a.append(self.record_a_aaaa(line_list, addition))
                elif "AAAA" in line_list:
                    z.records_aaaa.append(self.record_a_aaaa(line_list, addition))
                elif "CNAME" in line_list:
                    z.records_cname.append(self.record_ns_cname(line_list, addition))
                elif "NS" in line_list:
                    z.records_ns.append(self.record_ns_cname(line_list, addition))
                elif "SOA" in line_list:
                    z.dns_servers_zone.append(self.record_soa(line_list, addition))
                elif "MX" in line_list:
                    z.records_mx.append(self.record_mx_recor(line_list, addition))
        print(str(z))
        return z

    # Конвертирует время
    @staticmethod
    def time_convert(time_no_conv: str) -> int:
        if "w" in time_no_conv or "W" in time_no_conv:
            time = int(time_no_conv[:-1]) * 604800
        elif "d" in time_no_conv or "D" in time_no_conv:
            time = int(time_no_conv[:-1]) * 86400
        elif "h" in time_no_conv or "H" in time_no_conv:
            time = int(time_no_conv[:-1]) * 3600
        elif "m" in time_no_conv or "M" in time_no_conv:
            time = int(time_no_conv[:-1]) * 60
        else:
            time = int(time_no_conv)
        return time

    # Готов
    def record_soa(self, line: list, addition="") -> list:
        # [host, first_server, responsible,
        # serial_num, time_update, time_reset, time_ends, ttl_min]
        record = []
        inc = 0
        host = line[0]
        if host == "@":
            record.append(addition)
        else:
            if host[:-1] != ".":
                host += "." + addition
            record.append(host)
        if line[inc + 1] != "SOA":
            inc += 1
        for inc_1 in range(9):
            if inc_1 <= 3:
                record.append(line[inc + inc_1])
            else:
                conv_t = self.time_convert(line[inc + inc_1])
                record.append(conv_t)
        return record

    # Готов
    @staticmethod
    def record_mx_recor(line: list, addition="") -> list:
        # [host, priority, host2]
        record = []
        inc = 2
        host = line[0]
        if host == "@":
            record.append(addition)
        else:
            if host[:-1] != ".":
                host += "." + addition
            record.append(host)
        if line[1] != "MX":
            inc += 1
        record.append(line[inc])
        point_contin = line[inc + 1]
        if point_contin != ".":
            point_contin += "." + addition
        record.append(point_contin)
        return record

    # Готов
    @staticmethod
    def record_a_aaaa(line: list, addition="") -> list:
        # [host, ip]
        record = []
        inc = 1
        first = line[0]
        if first == "@":
            record.append(addition)
        else:
            if first[:-1] != ".":
                first += "." + addition
            record.append(first)
        if line[1] != "A" or "AAAA":
            inc += 1
        record.append(line[inc])
        return record

    # Готов
    @staticmethod
    def record_ns_cname(line: list, addition="") -> list:
        # [host\\server, rehost\host]
        record = []
        inc = 1
        first = line[0]
        if first == "@":
            record.append(addition)
        else:
            if first[:-1] != ".":
                first += "." + addition
            record.append(first)
        if line[1] != "CNAME" or "NS":
            inc += 1
        point_contin = line[inc]
        if point_contin[:-1] != ".":
            point_contin += "." + addition
        record.append(point_contin)
        return record
