from fastapi import FastAPI
from app.api import admin_user, forms , questions, answers, sections,logics


app = FastAPI(title="Forms API", version="1.0.0")

app.include_router(admin_user.router, prefix="/forms", tags=["Users"])
app.include_router(forms.router, prefix="/forms", tags=["Forms"])
app.include_router(sections.router,prefix="/sections",tags=["Section"])
app.include_router(questions.router,prefix="/questions",tags=["Questions"])
app.include_router(answers.router,prefix="/answers",tags=["Answers"])
app.include_router(logics.router,prefix="/logics",tags=["Logics"])

