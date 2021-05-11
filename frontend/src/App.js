import './App.css';
import Homepage from './pages/homepage/homepage.component';
import AddTransaction from './pages/add-transaction/add-transaction.component';
import Header from './components/header/header.component';
import { Switch, Route } from 'react-router-dom';

function App() {
  return (
    <div>
      <Header />
      <Switch>
        <Route path="/" component={Homepage} exact />
        <Route path="/add-transaction" component={AddTransaction} exact />
      </Switch>
    </div>
  );
}

export default App;
