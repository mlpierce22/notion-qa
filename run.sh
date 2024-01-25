frontend() {
    cd frontend
    bun run dev
}
backend() {
    cd backend
    python main.py
}

export -f frontend
export -f backend

parallel --line-buffer --halt now,fail=1 ::: frontend backend