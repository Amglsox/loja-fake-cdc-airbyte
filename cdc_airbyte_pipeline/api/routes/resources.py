import json
import logging

import psycopg2

from conf import Config
from faker import Faker
from flask import Blueprint
from flask import Response
from flask import request


obj_connection_postrges = Config()

routes = Blueprint("routes", __name__, url_prefix="/")


def execute_sql_command(query: str, params_query: tuple) -> str:
    rows = []
    retorno = ""
    try:
        logging.info("connect db")
        params = obj_connection_postrges._to_dict()
        conn = psycopg2.connect(**params)
        logging.info("connect ok db")
        cur = conn.cursor()
        logging.info("cursor ok db")
        cur.execute(query, params_query)
        logging.info("cursor execute ok")
        conn.commit()
        logging.info("commit")
        rows = cur.fetchall()
        for row in rows:
            logging.info(row)
        cur.close()
        logging.info("close db")

    except (Exception, psycopg2.DatabaseError) as error:
        logging.info(error)
    finally:
        logging.info(len(rows))
        if len(rows) > 0:
            retorno = "Cliente Existe"
        elif conn is not None:
            conn.close()
            retorno = "OK"
    return retorno


@routes.route("/", methods=["GET"])
@routes.route("/healthcheck", methods=["GET"])
def healthcheck() -> Response:
    logging.info("Start healthcheck")
    return Response(json.dumps({"Status": "running"}), status=200, mimetype="application/json")


@routes.route("/get_person", methods=["GET", "POST"])
def get_person() -> Response:
    sql = "SELECT * FROM public.tb_clientes WHERE username = %s"
    tuple_cliente = ("ucarvalho",)
    retorno = execute_sql_command(sql, tuple_cliente)
    return Response(
        json.dumps({"Status": "ok", "msg": retorno}),
        status=200,
        mimetype="application/json",
    )


@routes.route("/create_person", methods=["GET", "POST"])
def create_person() -> Response:
    fake = Faker("pt_BR")
    person = fake.profile()
    person = {
        "nome": person["name"],
        "dtNascimento": person["birthdate"].strftime("%Y-%m-%d"),
        "empresa": person["company"],
        "profissao": person["job"],
        "cpf": person["ssn"],
        "enderecoCompleto": person["residence"].replace("\n", " "),
        "logradouro": person["residence"].split("\n")[0],
        "bairro": person["residence"].split("\n")[1],
        "cep": person["residence"].split("\n")[2][:8],
        "cidade": person["residence"].split("\n")[2][9:].split("/")[0].strip(),
        "estado": person["residence"].split("\n")[2][9:].split("/")[1].strip(),
        "blood_group": person["blood_group"],
        "website": person["website"],
        "sexo": person["sex"],
        "mail": person["mail"],
        "username": person["username"],
        "address": person["address"],
        "pais": "Brasil",
    }
    sql = "SELECT * FROM public.tb_clientes WHERE mail = %s"
    tuple_cliente = (person["mail"],)
    retorno = execute_sql_command(sql, tuple_cliente)
    if retorno == "Cliente Existe":
        sql = """UPDATE public.tb_clientes
                SET profissao=%s, empresa=%s, blood_group=%s,
                website=%s, username=%s,
                sexo=%s, address=%s, dtnascimento=%s,
                cpf=%s, enderecocompleto=%s, logradouro=%s,
                bairro=%s, cep=%s, cidade=%s,
                estado=%s, pais=%s,
                update_at=CURRENT_TIMESTAMP
                WHERE mail=%s;"""
        tuple_cliente = (
            person["profissao"],
            person["empresa"],
            person["blood_group"],
            person["website"],
            person["username"],
            person["sexo"],
            person["address"],
            person["dtNascimento"],
            person["cpf"],
            person["enderecoCompleto"],
            person["logradouro"],
            person["bairro"],
            person["cep"],
            person["cidade"],
            person["estado"],
            person["pais"],
            person["mail"],
        )
        retorno = execute_sql_command(sql, tuple_cliente)
    else:
        sql = """INSERT INTO public.tb_clientes (profissao, empresa, blood_group, website, username, nome, sexo,
                 address, mail, dtnascimento, cpf, enderecocompleto, logradouro, bairro, cep, cidade, estado,
                 pais, create_at, update_at)
             VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
             CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);"""
        tuple_client = (
            person["profissao"],
            person["empresa"],
            person["blood_group"],
            person["website"],
            person["username"],
            person["nome"],
            person["sexo"],
            person["address"],
            person["mail"],
            person["dtNascimento"],
            person["cpf"],
            person["enderecoCompleto"],
            person["logradouro"],
            person["bairro"],
            person["cep"],
            person["cidade"],
            person["estado"],
            person["pais"],
        )
        retorno = execute_sql_command(sql, tuple_client)
    return Response(
        json.dumps({"data": {"Status": "ok", "person": retorno}}),
        status=200,
        mimetype="application/json",
    )


@routes.route("/delete_person/<mail>", methods=["DELETE"])
def delete_person(mail: str) -> Response:
    sql = "SELECT * FROM public.tb_clientes WHERE mail = %s"
    tuple_cliente = (mail,)
    retorno = execute_sql_command(sql, tuple_cliente)
    if retorno == "Cliente Existe":
        sql = "DELETE FROM public.tb_clientes WHERE mail = %s"
        tuple_cliente = (mail,)
        retorno = execute_sql_command(sql, tuple_cliente)
    return Response(
        json.dumps({"data": {"Status": "Delete", "person": mail}}),
        status=200,
        mimetype="application/json",
    )


@routes.route("/update_person/<mail>", methods=["PUT"])
def update_person(mail: str) -> Response:
    sql = """UPDATE public.tb_clientes
             SET profissao=%s, empresa=%s, blood_group=%s,
             website=%s, username=%s,
             sexo=%s, address=%s, dtnascimento=%s,
             cpf=%s, enderecocompleto=%s, logradouro=%s,
             bairro=%s, cep=%s, cidade=%s,
             estado=%s, pais=%s,
             update_at=CURRENT_TIMESTAMP
             WHERE mail=%s;"""

    tuple_cliente = (
        request.json.get("profissao"),
        request.json.get("empresa"),
        request.json.get("blood_group"),
        request.json.get("website"),
        request.json.get("username"),
        request.json.get("sexo"),
        request.json.get("address"),
        request.json.get("dtNascimento"),
        request.json.get("cpf"),
        request.json.get("enderecoCompleto"),
        request.json.get("logradouro"),
        request.json.get("bairro"),
        request.json.get("cep"),
        request.json.get("cidade"),
        request.json.get("estado"),
        request.json.get("pais"),
        mail,
    )
    retorno = execute_sql_command(sql, tuple_cliente)
    return Response(
        json.dumps({"data": {"Status": "Update", "person": mail, "callback": retorno}}),
        status=200,
        mimetype="application/json",
    )
