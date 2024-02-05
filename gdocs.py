import gspread
from oauth2client.service_account import ServiceAccountCredentials


def next_available_row(sheet):
    """Devuelve la próxima fila vacía en una spreadsheet"""
    str_list = list(filter(None, sheet.col_values(1)))
    return str(len(str_list) + 1)


def importar_gdocs():
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = ServiceAccountCredentials.from_json_keyfile_name("mpb_api.json", scope)

    client = gspread.authorize(creds)

    # if "Haikyuu" in fandom:
    #     path = "../../fics/hq/"
    # elif "Jujutsu" in fandom:
    #     path = "../../fics/jjk/"
    # elif "Trigun" in fandom:
    #     path = "../../fics/trigun/"
    # elif "Attorney" in fandom:
    #     path = "../../fics/aa/"
    # elif "One Piece" in fandom:
    #     path = "../../fics/op/"
    # elif "Shingeki" in fandom:
    #     path = "../../fics/snk/"
    # else:
    #     path = "../../fics/"
    hq = client.open("Haikyuu fic recs").worksheet("Sin leer")
    trigun = client.open("Haikyuu fic recs").worksheet("Trigun sin leer")
    op = client.open("various fic recs (sans hq)").worksheet("OP")
    aa = client.open("various fic recs (sans hq)").worksheet("AA")
    sk8 = client.open("various fic recs (sans hq)").worksheet("sk8")
    jjk = client.open("various fic recs (sans hq)").worksheet("jjk")
    snk = client.open("various fic recs (sans hq)").worksheet("snk")
    otros = client.open("various fic recs (sans hq)").worksheet("varios")

    return hq, trigun, op, aa, sk8, jjk, snk, otros
