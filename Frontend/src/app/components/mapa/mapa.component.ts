import { Component, OnInit, OnDestroy } from '@angular/core';
import * as L from 'leaflet';
import { ruta20, ruta40, ruta50 } from '../../data/rutas';
import { ServiceService } from '../../service.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-mapa',
  templateUrl: './mapa.component.html',
  styleUrls: ['./mapa.component.css'],
  standalone: true,
  imports: [CommonModule]  // Importamos CommonModule aqu
})
export class MapaComponent implements OnInit, OnDestroy {
  rutas: any[] = [];

  private map!: L.Map;
  private marker!: L.Marker;
  private routeCoordinates: any[] = []; // Coordenadas de la ruta
  private totalDistance: number = 0; // Distancia total de la ruta
  private totalDuration: number = 0; // Duración total de la ruta en ms
  private progress: number = 0; // Progreso de la ruta (de 0 a 1)
  private interval: any;
  private speedFactor: number = 0.30; // Factor para controlar la velocidad (en km/s)
  private currentRoute: string = 'ruta20'; // Ruta activa por defecto (puede cambiar a 'ruta40' o 'ruta50')

  constructor(private apiService: ServiceService) { }
  ngOnInit(): void {
    this.initMap();
    this.cargarRutas(); // Cargar rutas iniciales
    this.startCursorAnimation(); // Comienza la animación al cargar el mapa
  }

  ngOnDestroy(): void {
    // Limpiar el intervalo cuando el componente se destruye
    if (this.interval) {
      clearInterval(this.interval);
    }
  }

  private initMap(): void {
    this.map = L.map('map').setView([21.88, -102.30], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(this.map);
  }

  private cargarRutas(): void {
    this.apiService.getRutas().subscribe(
      (data) => {
        this.rutas = data;
        console.log(this.rutas); // Aquí puedes manejar las rutas obtenidas
      },
      (error) => {
        console.error('Error al cargar las rutas', error);
      }
    );
    const opciones = {
      style: {
        color: 'blue',
        weight: 4
      }
    };

    L.geoJSON(ruta20 as any, { ...opciones, style: { color: 'blue' } }).addTo(this.map);
    L.geoJSON(ruta40 as any, { ...opciones, style: { color: 'green' } }).addTo(this.map);
    L.geoJSON(ruta50 as any, { ...opciones, style: { color: '#9f1515' } }).addTo(this.map);

    // Al cargar las rutas, seleccionamos las coordenadas de la ruta activa
    this.updateRouteCoordinates();
  }

  private updateRouteCoordinates(): void {
    // Cambiar las coordenadas de la ruta según la ruta activa
    switch (this.currentRoute) {
      case 'ruta40':
        this.routeCoordinates = ruta40.features[0].geometry.coordinates[0];
        break;
      case 'ruta50':
        this.routeCoordinates = ruta50.features[0].geometry.coordinates[0];
        break;
      case 'ruta20':
      default:
        this.routeCoordinates = ruta20.features[0].geometry.coordinates[0];
        break;
    }

    // Calcular la distancia total de la ruta
    this.totalDistance = this.calculateRouteLength();
    this.totalDuration = this.totalDistance / this.speedFactor * 1000; // Convertir a milisegundos
  }

  private calculateRouteLength(): number {
    let totalDistance = 0;

    // Calcular la distancia total de la ruta
    for (let i = 0; i < this.routeCoordinates.length - 1; i++) {
      const start = this.routeCoordinates[i];
      const end = this.routeCoordinates[i + 1];

      // Calcular la distancia de cada segmento
      totalDistance += this.calculateDistance(start, end);
    }

    return totalDistance;
  }

  private calculateDistance(start: any, end: any): number {
    const R = 6371; // Radio de la Tierra en km
    const lat1 = start[1] * Math.PI / 180;
    const lat2 = end[1] * Math.PI / 180;
    const deltaLat = (end[1] - start[1]) * Math.PI / 180;
    const deltaLon = (end[0] - start[0]) * Math.PI / 180;

    const a = Math.sin(deltaLat / 2) * Math.sin(deltaLat / 2) +
      Math.cos(lat1) * Math.cos(lat2) *
      Math.sin(deltaLon / 2) * Math.sin(deltaLon / 2);
    
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c; // Distancia en km
  }

  private startCursorAnimation(): void {
    // Usamos una imagen de camión como icono
    const truckIcon = L.icon({
      iconUrl: '/assets/images/camion.png', // Ruta relativa desde la raíz del servidor
      iconSize: [32, 32], // Tamaño del icono
      iconAnchor: [16, 16], // Ancla del icono para centrarlo sobre el marcador
      popupAnchor: [0, -16] // Ajusta el popup si lo usas
    });

    // Crear el marcador con el icono personalizado
    this.marker = L.marker(this.routeCoordinates[0], {
      icon: truckIcon // Usamos el icono de camión
    }).addTo(this.map);

    // Mover el marcador a lo largo de la ruta de forma continua
    this.interval = setInterval(() => {
      this.progress += 0.001; // Aumenta el progreso del marcador a lo largo de la ruta

      if (this.progress >= 1) {
        this.progress = 0; // Reiniciar el recorrido al llegar al final
      }

      // Interpolar la posición del marcador a lo largo de la ruta
      const nextPoint = this.interpolateAlongRoute(this.progress);

      // Actualizar la posición del marcador
      this.marker.setLatLng([nextPoint[1], nextPoint[0]]);
    }, this.totalDuration / 1000); // Dividir el total de la duración entre los segmentos para mantener la velocidad constante
  }

  private interpolateAlongRoute(progress: number): any {
    const totalLength = this.routeCoordinates.length;
    const segmentProgress = progress * (totalLength - 1);
    const startIdx = Math.floor(segmentProgress);
    const endIdx = Math.ceil(segmentProgress);

    const start = this.routeCoordinates[startIdx];
    const end = this.routeCoordinates[endIdx];

    const fraction = segmentProgress - startIdx; // Proporción del segmento

    return this.interpolatePoint(start, end, fraction);
  }

  private interpolatePoint(start: any, end: any, fraction: number): any {
    const lat = start[1] + (end[1] - start[1]) * fraction;
    const lng = start[0] + (end[0] - start[0]) * fraction;
    return [lng, lat];
  }

  // Método para cambiar de ruta
  cambiarRuta(ruta: string): void {
    this.currentRoute = ruta;
    this.updateRouteCoordinates(); // Actualiza las coordenadas de la nueva ruta
    this.marker.setLatLng(this.routeCoordinates[0]); // Restablecer la posición del marcador
    this.progress = 0; // Reiniciar el progreso
  }
}

