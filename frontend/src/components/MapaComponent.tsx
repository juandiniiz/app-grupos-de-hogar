import React from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

delete (L.Icon.Default.prototype as any)._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const greenIcon = L.icon({
  iconUrl: 'data:image/svg+xml;base64,' + btoa(`<svg xmlns="http://www.w3.org/2000/svg" width="24" height="36" viewBox="0 0 24 36"><path fill="#66B97B" d="M12 0C5.4 0 0 5.4 0 12c0 9 12 24 12 24s12-15 12-24C24 5.4 18.6 0 12 0zm0 16c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4z"/></svg>`),
  iconSize: [24, 36],
  iconAnchor: [12, 36],
  popupAnchor: [0, -36],
})

interface MapPoint {
  id: number
  nombre: string
  apellidos?: string
  latitude: number
  longitude: number
  grupo_nombre?: string
}

interface Props {
  points: MapPoint[]
  height?: string
}

export default function MapaComponent({ points, height = '300px' }: Props) {
  const center: [number, number] = points.length > 0
    ? [points[0].latitude, points[0].longitude]
    : [39.47, -0.38]

  return (
    <div style={{ height }} className="rounded-lg overflow-hidden">
      <MapContainer center={center} zoom={12} style={{ height: '100%', width: '100%' }}>
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
        {points.map(p => (
          <Marker key={p.id} position={[p.latitude, p.longitude]} icon={greenIcon}>
            <Popup>
              <strong>{p.nombre}{p.apellidos ? ` ${p.apellidos}` : ''}</strong>
              {p.grupo_nombre && <><br />{p.grupo_nombre}</>}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  )
}
