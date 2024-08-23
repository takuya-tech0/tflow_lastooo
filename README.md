## Backend
・python -m venv .venv

・.venv/Scripts/activate

・pip install -r requirements.txt

・uvicorn app.main:app --reload

※ModuleNotFoundError: No module named 'app'というエラーが出たら、もう一度やれば直ります
※envファイルを設定→OPENAI_API_KEY=`your_api_key`を格納

https://platform.openai.com/api-keys

## Frontend
・npm install

・npm install framer-motion

・ルートディレクトリーに.envファイルを作成→NEXT_PUBLIC_API_URL=http://localhost:8000と入力

・npm run dev


