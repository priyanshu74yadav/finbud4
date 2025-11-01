import { motion } from "framer-motion"

export default function Footer() {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 1.2 }}
      className="border-t border-gray-200 bg-white/50 py-8 px-4 sm:px-6 lg:px-8 mt-20"
    >
      <div className="container mx-auto max-w-6xl">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <p className="text-sm text-gray-600">
            © FinBud 2025. All rights reserved.
          </p>
          <div className="flex items-center gap-6">
            <a
              href="#terms"
              className="text-sm text-gray-600 hover:text-[#6D28D9] transition-colors duration-200"
            >
              Terms
            </a>
            <span className="text-gray-300">|</span>
            <a
              href="#privacy"
              className="text-sm text-gray-600 hover:text-[#6D28D9] transition-colors duration-200"
            >
              Privacy
            </a>
          </div>
        </div>
      </div>
    </motion.footer>
  )
}

