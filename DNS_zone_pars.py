import argparse
import socket
from bitstring import BitArray



class Zone:
    name_zone = ""
    ttl = 0
    records_a =[]
    records_aaaa = []
    records_ns = []
    records_mx = []
    records_cname = []
    dns_servers_zone = []


class Zone_parse:

    def __init__(self, file_path):
        pass

    def generation_zone_object(self, path):
        z = Zone
        addition = ""
        with open(path, "r") as file_z:
            for line in file_z:
                line = line.replace("(", " ")
                line = line.replace(")", " ")
                line_list = line.split()
                if "$ORIGIN" == line_list[0]:
                    addition = line_list[1]
                elif "$TTL" == line_list[0]:
                    z.ttl = self.time_convert(line_list[1])
                elif "A" in line_list:
                    z.records_a.append(self.record_a_aaaa_ns_cname(line_list))
                elif "AAAA" in line_list:
                    z.records_aaaa.append(self.record_a_aaaa_ns_cname(line_list))
                elif "CNAME" in line_list:
                    z.records_cname.append(self.record_a_aaaa_ns_cname(line_list, addition))
                elif "NS" in line_list:
                    z.records_ns.append(self.record_a_aaaa_ns_cname(line_list, addition))
                elif "SOA" in line_list:
                    soa_zone, addition = self.record_soa(line_list, z.ttl)

    def time_convert(self, time_no_conv: str) -> int:
        time = 0
        if "w" or "W" in time_no_conv:
            time = int(time_no_conv[:-1]) * 604800
        elif "d" or "D" in time_no_conv:
            time = int(time_no_conv[:-1]) * 86400
        elif "h" or "H" in time_no_conv:
            time = int(time_no_conv[:-1]) * 3600
        elif "m" or "M" in time_no_conv:
            time = int(time_no_conv[:-1]) * 60
        return time

    @staticmethod
    def record_soa(line: list, ttl) -> list:
        # [host, first_server, responsible,
        # serial_num, time_update, time_reset, time_ends, ttl_min]
        record = []
        inc = 0
        inc_1 = 1
        record.append(line[inc])
        if line[inc + 1] != "SOA":
            inc += 1
        while inc_1 != 7:
            record.append(line[inc + inc_1])
            inc_1 += 1
        return record

    @staticmethod
    def record_mx_recor(line: list) -> list:
        # [host, priority, host2]
        record = []
        inc = 2
        record.append(line[0])
        if line[1] != "MX":
            inc += 1
        record.append(line[inc])
        record.append(line[inc + 1])
        return record

    @staticmethod
    def record_a_aaaa_ns_cname(line: list, addition=None) -> list:
        # [host\\server, ip\rehost\host]
        record = []
        inc = 2
        first = line[0]
        if first == "@" or first[:-1] != ".":
            record.append(addition )
        else:
            record.append(line[0])
        if line[1] != "A" or "AAAA" or "CNAME" or "NS":
            inc += 1
        point_contin = line[inc]
        record.append(point_contin)
        return record

    def huina(self, end, addition):
        if end == ".":
            
        return


class DNS_answer:
    query_doblicate = {}
    """
        create_hendler_pkg - Пакет собранный на основе [session: nnnn,
            QR: n, opcode: nnnn, AA: n, TC: n, RD: n, RA: n, rcode: nnnn, в этой строке n - "0" || "1"
            num_requests: nnnn, num_response: nnnn, nnnn, nnnn]
    """

    def __init__(self):
        pass
        # port, mode, file_zone_path = self.args_parse()

    def start_udp_mode(self, port):
        pass

    def start_tcp_mode(self, port):
        pass

    @staticmethod
    def args_parse():
        parser = argparse.ArgumentParser(description='DNS_script')
        parser.add_argument('-p', action="store", nargs="+", dest="ports", type=int, default=53,
                            help="Порт получения запросов, исхождения")
        parser.add_argument('-m', action="store", dest="mode", default="u",
                            help="t - tcp, u - udp, None - t && u")
        parser.add_argument('-f', action="store", dest="file", required=True,
                            help="Файл зон")
        args = parser.parse_args()
        return args.port, args.mode, args.file

    def create_data(self, pkg: list):
        pass

    def creat_answer(self, q_name: str, q_type: str):
        p = Zone_parse()


    def parse_pkg(self, pkg: str):
        query_last_point = 24
        pkg_list = self.parse_hendler_pkg(pkg)
        for i in range(int(pkg_list[8])):
            query_name, query_type, query_last_point = self.parse_query(pkg, query_last_point)

    # Парсит один запрос
    def parse_query(self, pkg: str, query_last_point: int) -> (str, str, int):
        pkg = pkg[query_last_point:]
        query_name = ""
        query_type = ""
        type_d = {1: "A", 28: "AAAA", 5: "CNAME", 15: "MX", 2: "NS", 6: "SOA"}
        i = 0
        j = 2
        counter = pkg[i:j]
        start_point = counter
        while counter != "00":
            counter = int(counter)
            i += 2
            j += 2
            if counter <= 64:
                while counter != 0:
                    query_name += chr(int(pkg[i:j], 16))
                    i += 2
                    j += 2
                    counter -= 1
                query_name += "."
                counter = pkg[i:j]
            elif counter >= 192:
                query_name += self.query_doblicate.get(pkg[i:j])
            else:
                print("Некорректный размер записи (более 64 символов)")
        if self.query_doblicate.get(query_name) is not None:
            self.query_doblicate.setdefault(start_point, query_name)

        for k in range(2):
            i += 2
            j += 2
            query_type += str(pkg[i:j])
        query_type = type_d.get(int(query_type))
        if query_type is None:
            print("Тип запроса не представляеться возможным для данного сервиса")

        query_last_point += j + 4
        return query_name[:-1], query_type, query_last_point

    # Здоровым людям не показывать
    def create_hendler_pkg(self, pack: list) -> str:
        packet = ""
        session = pack[0]
        s = pack[1] + pack[2] + pack[3] + pack[4] + pack[5]
        flags = str(int(s, 2).to_bytes(len(s) // 8, byteorder='big'))[4:6]
        s = pack[6] + "000" + pack[7]
        flags += str(int(s, 2).to_bytes(len(s) // 8, byteorder='big'))[4:6]
        num = pack[8] + pack[9] + pack[10] + pack[11]
        packet = session + flags + num
        return packet

    # Здоровым людям не показывать
    def parse_hendler_pkg(self, pack: str) -> list:
        pkg_data = []
        pkg_data.append(pack[0:4])  # session

        flags = pack[4:8]
        flags = BitArray(hex=flags)
        flags = flags.bin

        pkg_data.append(flags[0:1])  # QR
        pkg_data.append(flags[1:5])  # opcode
        pkg_data.append(flags[5:6])  # AA
        pkg_data.append(flags[6:7])  # TC
        pkg_data.append(flags[7:8])  # RD
        pkg_data.append(flags[8:9])  # RA
        pkg_data.append(flags[12:16])  # rcode
        pkg_data.append(pack[8:12])  #
        pkg_data.append(pack[12:16])  #
        pkg_data.append(pack[16:20])  #
        pkg_data.append(pack[20:24])  #

        return pkg_data


if __name__ == '__main__':
    dns = DNS_answer()
    pkg = "000201000001000000000000026531027275000002"
    print(dns.parse_pkg(pkg))
    # p = dns.parse_hendler_pkg(pkg)
    # pa = ['0002', '0', '0000', '0', '0', '1', '0', '0000', '0001', '0000', '0000', '0000']
    # z = dns.create_hendler_pkg(pa)
