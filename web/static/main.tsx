import { createRoot } from 'react-dom/client';
import Simulator from '../components/t7/simulator';
import '../app/globals.css';
import './static.css';

createRoot(document.getElementById('root')!).render(<Simulator />);
