import { useNavigate } from 'react-router-dom';
import AppShell from '../components/AppShell.jsx';
import Navbar from '../components/Navbar.jsx';
import HeroSection from '../components/HeroSection.jsx';
import PageTransition from '../components/PageTransition.jsx';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <AppShell>
      <Navbar />
      <PageTransition>
        <HeroSection onCta={() => navigate('/portal')} />
      </PageTransition>
    </AppShell>
  );
}
