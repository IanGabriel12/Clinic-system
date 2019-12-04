import services
import models

consulta = services.getConsultas()[0]

consulta.descricao = 'Suspeita de Tuberculose'
services.editarConsulta(consulta)