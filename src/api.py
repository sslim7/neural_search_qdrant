from fastapi import FastAPI, HTTPException, Query
from neural_searcher import NeuralSearcher

app = FastAPI(
    title="My API",
    description="This is a very fancy project, with auto docs for the API and everything",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc"
)

neural_searcher = NeuralSearcher(collection_name="startups")

@app.get("/api/search", summary="Search for startups", description="검색질의를 자연어로 입력하세요")
def search_startup(
    q: str = Query(..., description="검색질의를 자연어로 입력하세요"),
    skip: int = Query(0, description="페이지 시작 위치"),
    limit: int = Query(5, description="페이지 크기")
):
    try:
        return {"result": neural_searcher.search(text=q, skip=skip, limit=limit)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/search_city", summary="Search for startups in a specific city", description="검색질의를 자연어로 입력하고 도시명을 입력하세요")
def search_city(
    q: str = Query(..., description="검색질의를 자연어로 입력하세요"),
    city: str = Query(..., description="도시명을 입력하세요")
):
    try:
        return {"result": neural_searcher.search_with_filter(text=q, city=city)}
    except Exception as e:
        print(f"Error in /api/search_city: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/collections", summary="List all collections", description="모든 컬렉션을 나열합니다")
def list_collections():
    try:
        return {"collections": neural_searcher.list_collections()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/col_struct", summary="Get collection structure", description="특정 컬렉션의 구조를 가져옵니다")
def collection_structure():
    try:
        structure = neural_searcher.col_struct()
        return {"col_struct": structure}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/count_by_city", summary="Count results by city", description="특정 검색질의에 대한 결과를 도시별로 계산합니다")
def count_by_city(q: str = Query(..., description="검색질의를 자연어로 입력하세요")):
    try:
        city_counts = neural_searcher.count_by_city(text=q)
        return {"city_counts": city_counts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/count_all", summary="Count all documents", description="컬렉션의 모든 문서 개수를 계산합니다")
def count_all():
    try:
        total_count = neural_searcher.count_all()
        return {"total_count": total_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)