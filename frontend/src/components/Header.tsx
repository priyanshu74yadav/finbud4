import { Wallet, Menu } from "lucide-react"
import { Button } from "./ui/button"
import { motion } from "framer-motion"

export default function Header() {
  const menuItems = ["Overview", "Agents", "Insights", "Pricing"]

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50 shadow-soft"
    >
      <nav className="container mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="flex items-center gap-2 cursor-pointer"
          >
            <Wallet className="h-6 w-6 text-[#6D28D9]" />
            <span className="text-xl font-bold bg-gradient-to-r from-[#6D28D9] to-[#9333EA] bg-clip-text text-transparent">
              FinBud
            </span>
          </motion.div>

          {/* Menu Items - Desktop */}
          <div className="hidden md:flex items-center gap-8">
            {menuItems.map((item) => (
              <motion.a
                key={item}
                href={`#${item.toLowerCase()}`}
                whileHover={{ scale: 1.05 }}
                className="text-sm font-medium text-gray-700 hover:text-[#6D28D9] transition-colors duration-200 cursor-pointer"
              >
                {item}
              </motion.a>
            ))}
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="default"
              className="hidden sm:flex border-gray-300 hover:border-[#6D28D9] hover:text-[#6D28D9]"
            >
              Login
            </Button>
            <Button
              variant="default"
              size="default"
              className="hidden sm:flex"
            >
              Sign Up
            </Button>
            <Button
              variant="ghost"
              size="icon"
              className="md:hidden"
            >
              <Menu className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </nav>
    </motion.header>
  )
}

