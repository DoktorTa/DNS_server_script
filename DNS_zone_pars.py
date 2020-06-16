import argparse
import socket
from bitstring import BitArray
from Zone_parcer import Zone_parse


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
    z = Zone_parse()
    zone = z.generation_zone_object(r"zon_dns_p.txt")
    r, i, k = zone.serch_soa_addition("ns.example.com.")
    print(r, i, k)
    # dns = DNS_answer()
    # pkg = "000201000001000000000000026531027275000002"
    # print(dns.parse_pkg(pkg))
    # # p = dns.parse_hendler_pkg(pkg)
    # # pa = ['0002', '0', '0000', '0', '0', '1', '0', '0000', '0001', '0000', '0000', '0000']
    # # z = dns.create_hendler_pkg(pa)
