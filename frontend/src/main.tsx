import ReactDOM from 'react-dom/client';
import 'bootstrap/dist/css/bootstrap.min.css';
import QueryPage from './pages/QueryPage';


ReactDOM.createRoot(document.getElementById('root')!).render(
    <App />
)

function App() {

    return (
        <div 
            id="main-container"
            style= {{ height: "100%"}}
        >
            <QueryPage />
        </div>
    );
}