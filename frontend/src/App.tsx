import Header from "./components/Header"
import Hero from "./components/Hero"
import ChatPanel from "./components/ChatPanel"
import Footer from "./components/Footer"

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-purple-50/30 to-blue-50/30">
      <Header />
      <main>
        <Hero />
        <ChatPanel />
      </main>
      <Footer />
    </div>
  )
}

export default App

