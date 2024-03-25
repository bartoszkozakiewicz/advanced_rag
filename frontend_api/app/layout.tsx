import HeaderBar from "@/components/HeadingBar/HeadingBar";
import NavBar from "@/components/NavBar/NavBar";
import "./globals.css";
import NewsletterSection from "@/components/NewsletterSection/NewsletterSection";
import Footer from "@/components/Footer/Footer";
import Chat from "@/components/chat";
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <head />
      <body>
        <NavBar />
        <HeaderBar />
        {children}
        {/* <NewsletterSection /> */}
        <Footer />
      </body>
    </html>
  );
}
