import { Injectable, BadRequestException } from '@nestjs/common';
import { AstConditionDto, AstAnalysisResultDto, AstErrorDto } from './dto';

/**
 * Service zur Validierung und Verarbeitung von AST-Bedingungen
 */
@Injectable()
export class AstConditionService {
  /**
   * Validiert die übergebenen AST-Bedingungen
   * @param conditions Die zu validierenden AST-Bedingungen
   * @throws BadRequestException wenn die Bedingungen ungültig sind
   */
  validateConditions(conditions: AstConditionDto[]): void {
    if (!Array.isArray(conditions)) {
      throw new BadRequestException('AST conditions must be an array');
    }

    for (const condition of conditions) {
      if (!condition.type || !condition.message) {
        throw new BadRequestException('Each AST condition must have a type and a message');
      }

      this.validateConditionType(condition);
    }
  }

  /**
   * Validiert eine spezifische Bedingung basierend auf ihrem Typ
   * @param condition Die zu validierende Bedingung
   * @throws BadRequestException wenn die Bedingung ungültig ist
   */
  private validateConditionType(condition: AstConditionDto): void {
    const { type, parameters } = condition;

    // Validierung für gemeinsame Bedingungstypen
    if (type === 'common.recursion') {
      if (!parameters.functionName) {
        throw new BadRequestException('Recursion condition requires a functionName parameter');
      }
    } else if (type === 'common.dataType') {
      if (!parameters.dataType) {
        throw new BadRequestException('DataType condition requires a dataType parameter');
      }
    }
    // Validierung für Python-spezifische Bedingungstypen
    else if (type.startsWith('python.')) {
      this.validatePythonCondition(type, parameters);
    }
    // Validierung für Java-spezifische Bedingungstypen
    else if (type.startsWith('java.')) {
      this.validateJavaCondition(type, parameters);
    }
    // Validierung für C++-spezifische Bedingungstypen
    else if (type.startsWith('cpp.')) {
      this.validateCppCondition(type, parameters);
    }
    // Validierung für benutzerdefinierte Bedingungen
    else if (type === 'custom') {
      if (!parameters.code) {
        throw new BadRequestException('Custom condition requires a code parameter');
      }
    } else {
      throw new BadRequestException(`Unknown condition type: ${type}`);
    }
  }

  /**
   * Validiert Python-spezifische Bedingungen
   * @param type Der Typ der Bedingung
   * @param parameters Die Parameter der Bedingung
   * @throws BadRequestException wenn die Bedingung ungültig ist
   */
  private validatePythonCondition(type: string, parameters: any): void {
    switch (type) {
      case 'python.forLoop':
      case 'python.whileLoop':
      case 'python.listComprehension':
        // Diese Bedingungen benötigen keine speziellen Parameter
        break;
      case 'python.functionCall':
        if (!parameters.functionName) {
          throw new BadRequestException('FunctionCall condition requires a functionName parameter');
        }
        break;
      case 'python.import':
        if (!parameters.moduleName) {
          throw new BadRequestException('Import condition requires a moduleName parameter');
        }
        break;
      default:
        throw new BadRequestException(`Unknown Python condition type: ${type}`);
    }
  }

  /**
   * Validiert Java-spezifische Bedingungen
   * @param type Der Typ der Bedingung
   * @param parameters Die Parameter der Bedingung
   * @throws BadRequestException wenn die Bedingung ungültig ist
   */
  private validateJavaCondition(type: string, parameters: any): void {
    // Grundgerüst für Java-Bedingungen
    throw new BadRequestException('Java conditions are not yet implemented');
  }

  /**
   * Validiert C++-spezifische Bedingungen
   * @param type Der Typ der Bedingung
   * @param parameters Die Parameter der Bedingung
   * @throws BadRequestException wenn die Bedingung ungültig ist
   */
  private validateCppCondition(type: string, parameters: any): void {
    // Grundgerüst für C++-Bedingungen
    throw new BadRequestException('C++ conditions are not yet implemented');
  }

  /**
   * Serialisiert AST-Bedingungen für die Übergabe an Container
   * @param conditions Die zu serialisierenden AST-Bedingungen
   * @returns Die serialisierten AST-Bedingungen als JSON-String
   */
  serializeConditions(conditions: AstConditionDto[]): string {
    return JSON.stringify(conditions);
  }

  /**
   * Deserialisiert AST-Analyseergebnisse aus dem Container
   * @param resultsJson Die zu deserialisierenden AST-Analyseergebnisse als JSON-String
   * @returns Die deserialisierten AST-Analyseergebnisse
   * @throws BadRequestException wenn die Deserialisierung fehlschlägt
   */
  deserializeResults(resultsJson: string): AstAnalysisResultDto {
    try {
      return JSON.parse(resultsJson);
    } catch (error) {
      throw new BadRequestException({
        message: 'Failed to parse AST analysis results',
        code: 'AST_PARSE_ERROR',
        error: error.message
      });
    }
  }

  /**
   * Erstellt ein Fehlerergebnis für die AST-Analyse
   * @param error Der Fehler
   * @returns Das Fehlerergebnis
   */
  createErrorResult(error: AstErrorDto): AstAnalysisResultDto {
    return {
      conditions: [],
      passed: false,
      score: 0,
      error: `${error.code}: ${error.message}`
    };
  }
}
