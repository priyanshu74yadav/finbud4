import { Mic, Send } from "lucide-react"
import { Button } from "./ui/button"
import { Input } from "./ui/input"
import { Card, CardContent } from "./ui/card"
import { motion } from "framer-motion"
import { useState } from "react"

export default function ChatPanel() {
  const [inputValue, setInputValue] = useState("")
  const options = [
    "Portfolio Analysis",
    "Stock Prediction",
    "Budget Planning",
    "Risk Assessment",
  ]

  return (
    <section className="py-6 px-4 sm:px-6 lg:px-8">
      <div className="container mx-auto max-w-3xl">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.8 }}
        >
          <Card className="bg-white/90 backdrop-blur-sm border-gray-200 shadow-glass">
            <CardContent className="p-6 sm:p-8">
              {/* Chat Input Area */}
              <div className="flex items-center gap-3 mb-2">
                <Input
                  type="text"
                  placeholder="Ask FinBud anything about finance..."
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  className="flex-1 bg-white/80"
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      // Handle send
                      setInputValue("")
                    }
                  }}
                />
               
                <Button
                  size="icon"
                  variant="default"
                  className="bg-gradient-to-r from-[#6D28D9] to-[#9333EA]"
                  aria-label="Send message"
                  onClick={() => setInputValue("")}
                >
                  <Send className="h-5 w-5" />
                </Button>
              </div>

              
             
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </section>
  )
}

