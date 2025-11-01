# FinBud Agent - Frontend

A modern, clean React frontend for FinBud Agent built with TypeScript, Tailwind CSS, and shadcn/ui components.

## Features

- 🎨 Light futuristic aesthetic with purple/blue accents
- 📱 Fully responsive design
- ✨ Smooth animations with Framer Motion
- 🧩 Modular component architecture
- 🎯 shadcn/ui components for consistent UI

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## Tech Stack

- **React 18** with TypeScript
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **shadcn/ui** - Re-usable component library
- **Framer Motion** - Animation library
- **Lucide React** - Icon library

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # shadcn/ui components
│   │   ├── Header.tsx   # Navigation header
│   │   ├── Hero.tsx     # Hero section
│   │   ├── ChatPanel.tsx # Main chat interface
│   │   └── Footer.tsx   # Footer component
│   ├── lib/
│   │   └── utils.ts     # Utility functions
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── tailwind.config.js
└── vite.config.ts
```

## Components

### Header
Fixed navigation bar with logo, menu items, and authentication buttons.

### Hero
Landing section with headline, subtext, and call-to-action buttons.

### ChatPanel
Centered chat interface with input field, voice button, and option buttons for quick actions.

### Footer
Minimal footer with copyright and legal links.

