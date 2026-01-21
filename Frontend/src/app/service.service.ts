// api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ServiceService {

  private baseUrl = 'http://localhost:5000'; // URL base de tu backend

  constructor(private http: HttpClient) { }

  // Obtener todas las rutas
  getRutas(): Observable<any> {
    return this.http.get(`${this.baseUrl}/rutas`);
  }

  // Obtener una ruta por ID
  getRuta(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/rutas/${id}`);
  }

  // Crear una nueva ruta
  createRuta(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/rutas`, data);
  }

  // Obtener todas las unidades
  getUnidades(): Observable<any> {
    return this.http.get(`${this.baseUrl}/unidades`);
  }

  // Crear una nueva unidad
  createUnidad(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/unidades`, data);
  }

}
