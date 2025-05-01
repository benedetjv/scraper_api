app = FastAPI()
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from ranking import buscar_posicao_furia, buscar_top_30
from lineup import buscar_lineup_furia
from noticias import buscar_noticias
from calendario import buscar_partida_furia_hoje

@app.get("/")
def root():
    return {"status": "FURIA API ativa."}

@app.get("/ranking/posicao")
def get_posicao():
    try:
        texto = buscar_posicao_furia()
        return {"texto": texto}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/ranking/top30")
def get_top30():
    try:
        dados = buscar_top_30()
        return {"top30": dados if isinstance(dados, list) else str(dados)}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/lineup")
def get_lineup():
    try:
        jogadores, coach = buscar_lineup_furia()
        return {"jogadores": jogadores, "coach": coach}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/noticias")
def get_noticias():
    try:
        noticias = buscar_noticias()
        return {"noticias": noticias}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})

@app.get("/calendario/hoje")
def get_calendario():
    try:
        resultado = buscar_partida_furia_hoje()
        return {"jogos": resultado}
    except Exception as e:
        return JSONResponse(status_code=500, content={"erro": str(e)})
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("scraper_api:app", host="0.0.0.0", port=8080)

