import { communityUrl } from "../config/webinars";
import SiteHeader from "../components/SiteHeader";
import Hero from "../components/Hero";
import Countdown from "../components/Countdown";
import WebinarList from "../components/WebinarList";
import Mentors from "../components/Mentors";
import HowItWorks from "../components/HowItWorks";
import FAQ from "../components/FAQ";
import InfoForm from "../components/InfoForm";
import Footer from "../components/Footer";
import Reveal from "../components/Reveal";
import { useDocumentMeta } from "../lib/seo";

export default function Home() {
  useDocumentMeta(
    "Ekim 2026 Avustralya'da Doktorluk Webinar Takvimi | AUSCAMP",
    "Avustralya'da doktorluk kariyeri düşünen hekimler için AUSCAMP'in Ekim 2026 ücretsiz webinar takvimi. Duyuru topluluğuna katıl."
  );

  return (
    <div className="flex min-h-screen w-full flex-col">
      <SiteHeader />
      <main className="flex-1">
        <Hero />
        <div className="mx-auto w-full max-w-5xl">
          <Reveal>
            <Countdown />
          </Reveal>
          <Reveal>
            <WebinarList />
          </Reveal>
        </div>
        <Reveal>
          <Mentors />
        </Reveal>
        <div className="mx-auto w-full max-w-5xl">
          <Reveal>
            <HowItWorks />
          </Reveal>
          <Reveal>
            <FAQ />
          </Reveal>
        </div>
        <Reveal>
          <InfoForm groupUrl={communityUrl} groupContentName="bilgi-kutusu-topluluk" />
        </Reveal>
      </main>
      <Footer />
    </div>
  );
}
