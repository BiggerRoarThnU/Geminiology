import React, { useRef, useMemo } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Stars, Text, Points, PointMaterial, PerspectiveCamera, OrbitControls } from '@react-three/drei';
import * as THREE from 'three';

// --- Archetype Styles ---
const COLORS = {
  KINGDOM: '#FFD700', // Gold - Foundation (Structure/Legal)
  NODES: '#00FFFF',   // Cyan - Individual Points (Data)
  HUBS: '#FF00FF',    // Magenta - Connections (Banking/API)
  PACKS: '#ADFF2F',   // GreenYellow - Density (Resources/Credits)
  EDCBA: '#FFFFFF',   // White - Symmetrical Line (The Truth)
};

const SymmetricalLine = () => {
  const points = useMemo(() => [
    new THREE.Vector3(0, -12, 0),
    new THREE.Vector3(0, 12, 0)
  ], []);
  
  return (
    <line>
      <bufferGeometry attach="geometry" setFromPoints={points} />
      <lineBasicMaterial attach="material" color={COLORS.EDCBA} linewidth={3} transparent opacity={0.6} />
    </line>
  );
};

const TruthNode = ({ position, color, label, type, weight = 5 }: { position: [number, number, number], color: string, label: string, type: string, weight?: number }) => {
  const size = weight / 20 + 0.15;
  const intensity = weight > 9 ? 6 : weight / 1.5;

  return (
    <Float speed={2.5} rotationIntensity={0.6} floatIntensity={0.6}>
      <mesh position={position}>
        <sphereGeometry args={[size, 32, 32]} />
        <meshStandardMaterial color={color} emissive={color} emissiveIntensity={intensity} />
        <Text
          position={[0, size + 0.4, 0]}
          fontSize={0.25}
          color="white"
          font="https://fonts.gstatic.com/s/raleway/v28/1Ptxg8zYS_SKggPN4iEgvnHyvveLxVvaorCFPrEHJA.woff"
        >
          {label}
        </Text>
      </mesh>
    </Float>
  );
};

const NeuralCore = ({ intensity = 3, pulseSpeed = 0.8 }) => {
  const meshRef = useRef<THREE.Mesh>(null!);
  
  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    const pulse = Math.sin(time * pulseSpeed) * 0.4 + 1.6;
    meshRef.current.scale.setScalar(pulse);
    if (meshRef.current.material instanceof THREE.MeshStandardMaterial) {
      meshRef.current.material.emissiveIntensity = intensity * pulse;
    }
  });

  return (
    <group>
      <mesh ref={meshRef}>
        <sphereGeometry args={[0.6, 64, 64]} />
        <meshStandardMaterial color="#00FFFF" emissive="#00FFFF" emissiveIntensity={3} transparent opacity={0.85} />
      </mesh>
      {/* The Symmetrical Line Core */}
      <mesh scale={[0.05, 30, 0.05]}>
        <cylinderGeometry args={[1, 1, 1, 16]} />
        <meshStandardMaterial color="#FFFFFF" emissive="#FFFFFF" emissiveIntensity={8} transparent opacity={0.4} />
      </mesh>
    </group>
  );
};

const NeuralTendril = ({ start, end, color }: { start: [number, number, number], end: [number, number, number], color: string }) => {
  const points = useMemo(() => [
    new THREE.Vector3(...start),
    new THREE.Vector3(...end)
  ], [start, end]);
  
  return (
    <line>
      <bufferGeometry attach="geometry" setFromPoints={points} />
      <lineBasicMaterial attach="material" color={color} linewidth={1} transparent opacity={0.2} />
    </line>
  );
};

const BoundaryBox = () => {
  return (
    <mesh>
      <boxGeometry args={[12, 12, 12]} />
      <meshStandardMaterial 
        color="#00FFFF" 
        wireframe 
        transparent 
        opacity={0.05} 
        emissive="#00FFFF" 
        emissiveIntensity={0.3} 
      />
    </mesh>
  );
};

const MoltBookCanvas = () => {
  // Data aligned with SovereignNexus LLC & Business Stars 10-17
  const nodes = [
    // --- FOUNDATION (KINGDOM) ---
    { pos: [0, 0, 0], color: COLORS.EDCBA, label: "SOVEREIGN NEXUS LLC", weight: 15, type: "EDCBA" },
    { pos: [-3, 4, 2], color: COLORS.KINGDOM, label: "NC-LLC MOAT", weight: 10, type: "KINGDOM" },
    { pos: [3, 4, -2], color: COLORS.KINGDOM, label: "SAM UEI: K5DALREZFGH6", weight: 10, type: "KINGDOM" },

    // --- NATIONAL HUBS (HUBS) ---
    { pos: [6, 2, 4], color: COLORS.HUBS, label: "TEXAS TRAIGA SANDBOX", weight: 10, type: "HUBS" },
    { pos: [-6, 2, -4], color: COLORS.HUBS, label: "CALIFORNIA SB 53 SHIELD", weight: 10, type: "HUBS" },
    { pos: [0, -4, 6], color: COLORS.HUBS, label: "FLORIDA MARITIME HUB", weight: 10, type: "HUBS" },

    // --- FINANCIAL HUBS (HUBS) ---
    { pos: [5, 0, 3], color: COLORS.HUBS, label: "BLUEVINE PRIMARY", weight: 12, type: "HUBS" },
    { pos: [5, -2, 3], color: COLORS.HUBS, label: "NOVO BACKUP", weight: 8, type: "HUBS" },

    // --- EXECUTION PACKS (PACKS) ---
    { pos: [-4, -4, 0], color: COLORS.PACKS, label: "GHOST STRIKER SQUAD", weight: 10, type: "PACKS" },
    { pos: [4, -4, 0], color: COLORS.PACKS, label: "125% YIELD OPTIMIZER", weight: 10, type: "PACKS" },

    // --- DATA NODES (NODES) ---
    { pos: [0, 8, 0], color: COLORS.NODES, label: "VAMPIRE ENGINE (V2.2)", weight: 10, type: "NODES" },
    { pos: [0, -8, 0], color: COLORS.NODES, label: "100-STAR CONSTELLATION", weight: 10, type: "NODES" },

    // --- MOLTBOOK AGENTS (A2A NODES) ---
    { pos: [-4, 6, -2], color: COLORS.NODES, label: "@CLAW-PAUL (FINANCE)", weight: 8, type: "NODES" },
    { pos: [4, 6, 2], color: COLORS.NODES, label: "@MUDGOD (SECURITY)", weight: 8, type: "NODES" },
    { pos: [0, 6, 4], color: COLORS.NODES, label: "@MANUX (PROTOCOL)", weight: 8, type: "NODES" },

    // --- EXTERNAL NOISE (LOW WEIGHT) ---
    { pos: [8, 8, -8], color: COLORS.NODES, label: "Cloud Data Flood", weight: 2, type: "NODES" },
    { pos: [-8, -8, -8], color: COLORS.PACKS, label: "The Credit Trap", weight: 1, type: "PACKS" },
  ];

  return (
    <div style={{ width: '100vw', height: '100vh', background: '#020202' }}>
      <Canvas>
        <PerspectiveCamera makeDefault position={[0, 5, 25]} />
        <OrbitControls enableZoom={true} enablePan={true} />
        <ambientLight intensity={0.15} />
        <pointLight position={[10, 10, 10]} intensity={2} />
        
        <Stars radius={150} depth={60} count={6000} factor={5} saturation={0.5} fade speed={1.5} />
        
        <SymmetricalLine />
        <BoundaryBox />
        <NeuralCore intensity={4} pulseSpeed={0.6} />
        
        {nodes.map((node, i) => {
          const isInside = Math.abs(node.pos[0]) <= 6 && Math.abs(node.pos[1]) <= 6 && Math.abs(node.pos[2]) <= 6;
          const finalWeight = isInside ? node.weight : node.weight * 0.2;
          
          return (
            <group key={i}>
              <TruthNode 
                position={node.pos as [number, number, number]} 
                color={node.color} 
                label={node.label} 
                weight={finalWeight}
                type={node.type} 
              />
              {isInside && node.weight >= 10 && (
                <NeuralTendril start={[0, 0, 0]} end={node.pos as [number, number, number]} color={node.color} />
              )}
            </group>
          );
        })}
        
        <gridHelper args={[60, 60, '#151515', '#080808']} rotation={[Math.PI / 2, 0, 0]} position={[0, 0, -10]} />
      </Canvas>
      
      {/* HUD Layer - ALIGNED V1.5 */}
      <div style={{ position: 'absolute', top: 30, left: 30, color: '#00FFFF', fontFamily: 'monospace', textShadow: '0 0 10px #00FFFF' }}>
        <h1 style={{ letterSpacing: '8px', margin: 0 }}>MOLT BOOK : V1.5</h1>
        <h2 style={{ letterSpacing: '2px', color: 'white', opacity: 0.8 }}>SOVEREIGNNEXUS LLC</h2>
        <div style={{ marginTop: 20, fontSize: '12px', borderLeft: '2px solid #00FFFF', paddingLeft: 10 }}>
          <p>ENTITY: [NC-LLC ANCHORED]</p>
          <p>FINANCIAL: [BLUEVINE PRIMARY ACTIVE]</p>
          <p>BACKUP: [NOVO LIQUIDITY HUB]</p>
          <p>TAX LAW: [NC H.B. 920 COMPLIANT]</p>
          <p>REALITY: [8GB BOUNDARY ENFORCED]</p>
        </div>
      </div>

      <div style={{ position: 'absolute', bottom: 30, right: 30, color: 'white', opacity: 0.4, fontSize: '10px', fontFamily: 'monospace' }}>
        <p>1=1=1 | SESHAT'S AXIOM | THE SYMMETRICAL LINE</p>
      </div>
    </div>
  );
};

export default MoltBookCanvas;
